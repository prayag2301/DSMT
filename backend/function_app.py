import azure.functions as func
import datetime
import json
import logging
import pickle
import pandas as pd


app = func.FunctionApp()

        
@app.route(route="score_model", auth_level=func.AuthLevel.ANONYMOUS)
def score_model(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the incoming JSON payload
        req_body = req.get_json()
        logging.info(f"Request payload: {req_body}")
        
        # Extract the features from the request
        total_qty = float(req_body.get("total_qty", 0))  # Ensure total_qty is numeric
        
        # List of all expected features
        suppliers = ['Aromatico', 'Beans Inc.', 'Fair Trade AG', 'Farmers of Brazil', 'Handelskontor Hamburg']
        warehouses = ['Amsterdam - RR', 'Barcelona - RR', 'Hamburg - RR', 'Istanbul - RR', 'London - RR', 'Nairobi - RR', 'Naples - RR']
        items = ['Arabica', 'Excelsa', 'Liberica', 'Maragogype', 'Maragogype Type B', 'Robusta']
        set_warehouses = ['Barcelona - RR', 'Hamburg - RR', 'Istanbul - RR', 'London - RR', 'Nairobi - RR', 'Naples - RR']
        
        # Construct the feature dictionary with defaults (0 for one-hot encoded features)
        data = {
            "total_qty": [total_qty],
        }
        
        # Add supplier one-hot encoding
        for supplier in suppliers:
            data[f'supplier_{supplier}'] = [1 if req_body.get(f"supplier_{supplier}", 0) == 1 else 0]
        
        # Add warehouse one-hot encoding
        for warehouse in warehouses:
            data[f'warehouse_{warehouse}'] = [1 if req_body.get(f"warehouse_{warehouse}", 0) == 1 else 0]
        
        # Add item one-hot encoding
        for item in items:
            data[f'item_{item}'] = [1 if req_body.get(f"item_{item}", 0) == 1 else 0]
        
        # Add set_warehouse one-hot encoding
        for set_warehouse in set_warehouses:
            data[f'set_warehouse_{set_warehouse}'] = [1 if req_body.get(f"set_warehouse_{set_warehouse}", 0) == 1 else 0]

        # Convert to DataFrame
        payload = pd.DataFrame(data)
        
        # Log the constructed payload
        logging.info(f"Constructed payload: {payload}")

        # Load the model
        model_path = './models/FINAL_best_model.pkl'
        with open(model_path, 'rb') as model_file:
            gridSearch = pickle.load(model_file)

        # Predict using the model
        prediction = gridSearch.predict(payload)[0]
        
        # Return the prediction
        response = {
            "message": "Model scored successfully",
            "avg_prediction": prediction,
            "status_code": 200,
        }
        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")
    
    except Exception as e:
        logging.error(f"Error during scoring: {str(e)}")
        response = {
            "message": "An error occurred during prediction",
            "error": str(e),
            "status_code": 500,
        }
        return func.HttpResponse(json.dumps(response), status_code=500, mimetype="application/json")
