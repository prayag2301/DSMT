import azure.functions as func
import datetime
import json
import logging
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import pickle

app = func.FunctionApp()

# Define the model class (replace with your actual model class)
class ANNDaysLate(nn.Module):
    def __init__(self):
        super(ANNDaysLate, self).__init__()
        # Define your model layers here
        # Input layer
        self.input = nn.Linear(30, 80)
        
        # Hidden layers
        self.hidden1 = nn.Linear(80, 160)
        self.hidden2 = nn.Linear(160, 180)
        self.hidden3 = nn.Linear(180, 110)
        self.hidden4 = nn.Linear(110, 64)
        self.hidden5 = nn.Linear(64, 32)
        
        # Dropout layers
        self.dropout1 = nn.Dropout(0.1)
        self.dropout2 = nn.Dropout(0.1)
        self.dropout3 = nn.Dropout(0.1)
        self.dropout4 = nn.Dropout(0.1)
        self.dropout5 = nn.Dropout(0.1)
        
        # Output layer
        self.output = nn.Linear(32, 1)

    def forward(self, x):
        total_qty = x[:, 0].view(-1, 1)
        x = F.relu(self.input(x))
        x = self.dropout1(x)
        x = F.relu(self.hidden1(x))
        x = self.dropout2(x)
        x = F.relu(self.hidden2(x))
        x = self.dropout3(x)
        x = F.relu(self.hidden3(x))
        x = self.dropout4(x)
        x = F.relu(self.hidden4(x))
        x = self.dropout5(x)
        x = F.relu(self.hidden5(x))
        x = self.output(x)  # No activation function for the output layer
        
        # Apply the rule to set days_late to 0 if total_qty is 0
        x = torch.where(total_qty == 0, torch.tensor(0.0, device=x.device), x)
        
        return x
torch.serialization.add_safe_globals({'ANNDaysLate': ANNDaysLate})

@app.route(route="score_model", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def score_model(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Extract parameters from the request body
        req_body = req.get_json()
        total_qty = req_body.get('total_qty', [0])[0]
        
        # Check for missing parameters
        if total_qty is None:
            raise ValueError("Missing required parameters.")
        
        # Convert total_qty to numeric
        try:
            total_qty = int(total_qty)
        except ValueError:
            raise ValueError("Quantity must be a numeric value.")
        
        # List of all expected features
        suppliers = ['Aromatico', 'Beans Inc.', 'Fair Trade AG', 'Farmers of Brazil', 'Handelskontor Hamburg']
        warehouses = ['Amsterdam - RR', 'Barcelona - RR', 'Hamburg - RR', 'Istanbul - RR', 'London - RR', 'Nairobi - RR', 'Naples - RR']
        items = ['Arabica', 'Excelsa', 'Liberica', 'Maragogype', 'Maragogype Type B', 'Robusta']
        set_warehouses = ['Barcelona - RR', 'Hamburg - RR', 'Istanbul - RR', 'London - RR', 'Nairobi - RR', 'Naples - RR']
        item_list = ['Excelsa', 'Liberica', 'Maragogype', 'Maragogype Type B', 'Robusta']
        
        # Construct the feature dictionary with defaults (0 for one-hot encoded features)
        data = {
            "total_qty": [total_qty],
        }
        
        # Add supplier one-hot encoding
        for s in suppliers:
            data[f'supplier_{s}'] = req_body.get(f'supplier_{s}', [0])
        
        # Add warehouse one-hot encoding
        for w in warehouses:
            data[f'warehouse_{w}'] = req_body.get(f'warehouse_{w}', [0])
        
        # Add item one-hot encoding
        for i in items:
            data[f'item_{i}'] = req_body.get(f'item_{i}', [0])
        
        # Add set_warehouse one-hot encoding
        for set_w in set_warehouses:
            data[f'set_warehouse_{set_w}'] = req_body.get(f'set_warehouse_{set_w}', [0])
        
        # Add item_list one-hot encoding
        for name in item_list:
            data[f'item_name_{name}'] = req_body.get(f'item_name_{name}', [0])
            
        # Ensure all 30 features are included
        all_features = ['total_qty'] + [f'supplier_{s}' for s in suppliers] + [f'warehouse_{w}' for w in warehouses] + [f'item_{i}' for i in items] + [f'set_warehouse_{sw}' for sw in set_warehouses] + [f'item_name_{name}' for name in item_list]
        for feature in all_features:
            if feature not in data:
                data[feature] = [0]

        print(data)
        # Convert to DataFrame
        payload = pd.DataFrame(data)
        
        # Log the constructed payload
        logging.info(f"Constructed payload: {payload}")

        # Load the model
        model_path = "./models/ANN.pkl"
        # Create an instance of the model
        model = ANNDaysLate()
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        
        # Ensure the model is in evaluation mode
        model.eval()
        
        # Convert the test input to a PyTorch tensor
        test_input_tensor = torch.tensor(payload.values).float()
        
        print(test_input_tensor.shape)
        
        # Make predictions
        with torch.no_grad():
            predictions = model(test_input_tensor)
        
        avg_prediction = predictions.numpy()[0][0]
        print(avg_prediction)
        
        # Return the prediction
        response = {
            "message": "Model scored successfully",
            "avg_prediction": float(avg_prediction),  # Convert to float for JSON serialization
            "status_code": 200,
        }
        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")
    
    except ValueError as ve:
        logging.error(f"Value error during scoring: {str(ve)}")
        response = {
            "message": "Invalid input",
            "error": str(ve),
            "status_code": 400,
        }
        return func.HttpResponse(json.dumps(response), status_code=400, mimetype="application/json")
    
    except Exception as e:
        logging.error(f"Error during scoring: {str(e)}")
        response = {
            "message": "An error occurred during prediction",
            "error": str(e),
            "status_code": 500,
        }
        return func.HttpResponse(json.dumps(response), status_code=500, mimetype="application/json")
