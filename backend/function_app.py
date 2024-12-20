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

    gbm700 = pickle.load(open('./models/gbm_n700_depth3_lr0.01.pkl', 'rb')) # Gradient Boosting Model (TUNED MODEL)

    lr = pickle.load(open('./models/lr_a1_it1000_sol-auto_ridge.pkl', 'rb'))    # Linear Regression Model

    rf = pickle.load(open('./models/rf_n600_depth8_split2_leaf1_sqrt_regressor.pkl', 'rb')) # Random Forest Model

    

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
    prediction_gbm700 =  gbm700.predict(payload)[0]
    prediction_lr = lr.predict(payload)[0]
    prediction_rf =  rf.predict(payload)[0]

  # Calculate the average prediction
    count = 0
    total_prediction = 0


    if prediction_gbm700 is not None and prediction_gbm700 >= 0:
        count += 1
        total_prediction += prediction_gbm700

    if prediction_lr is not None and prediction_lr >= 0:
        count += 1
        total_prediction += prediction_lr

    if prediction_rf is not None and prediction_rf >= 0:
        count += 1
        total_prediction += prediction_rf

    if count > 0:
        avg_prediction = total_prediction / count
    else:
        avg_prediction = None  # Something went wrong

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
        "prediction_gbm700": prediction_gbm700,
        "prediction_lr": prediction_lr,
        "prediction_rf": prediction_rf,        
        "avg_prediction": avg_prediction,
        "status_code": 200
        })
        