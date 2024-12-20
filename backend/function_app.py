import azure.functions as func
import datetime
import json
import logging
import pickle
import pandas as pd


app = func.FunctionApp()

        
@app.route(route="score_model", auth_level=func.AuthLevel.ANONYMOUS)
def score_model(req: func.HttpRequest) -> func.HttpResponse:
    
    # Getting supplier and quantity from request
    supplier = req.params.get('supplier')
    quantity = req.params.get('quantity')
    
    # Load Models
    #gbm = pickle.load(open('./models/gbm_500.pkl', 'rb')) # Gradient Boosting Model (INITAL MODEL)

    gridSearch = pickle.load(open('./models/newbest_model.pkl', 'rb')) # Gradient Boosting Model (TUNED MODEL)

    # lr = pickle.load(open('./models/lr_a1_it1000_sol-auto_ridge.pkl', 'rb'))    # Linear Regression Model

    # rf = pickle.load(open('./models/rf_n600_depth8_split2_leaf1_sqrt_regressor.pkl', 'rb')) # Random Forest Model

    

    # Define the possible suppliers
    suppliers = ['Aromatico', 'Beans Inc.', 'Fair Trade AG', 'Farmers of Brazil', 'Handelskontor Hamburg']
    
    # Create a dictionary for the DataFrame
    data = {
        "total_qty": [quantity],
    }
    
    # Add supplier one-hot encoding to the dictionary
    for s in suppliers:
        data[f'd_{s}'] = [1 if s == supplier else 0]
    
    # Create the DataFrame
    payload = pd.DataFrame(data)
    
    # Calculate the prediction
    prediction_GRID_SearchCV =  gridSearch.predict(payload)[0]
  

  # Calculate the average prediction

    avg_prediction = prediction_GRID_SearchCV
   
    if avg_prediction is None:
        return json.dumps({
            "message": "Model could not be scored",
            "status_code": 500
        })
        
    # Log the prediction
    logging.warning(f"The Average Predictions of the {count} models is: {avg_prediction}") 
    
    return json.dumps({
        "message": f"""Model scored successfully with quantity: {quantity} 
        and supplier: {supplier}""",       
        "avg_prediction": avg_prediction,
        "status_code": 200
        })
        