from typing import Union
from fastapi import FastAPI
import pandas as pd
import numpy as np
import os
import __main__
"""
cd Projecto-Final-ML/app
fastapi dev main.py"""

"""    server   Server started at 
    server   Documentation at 
"""
""" parar ctrl C"""
import sys
import os

# Añadir el directorio donde está tool_preprocess_onehot.py
sys.path.append(os.path.abspath("../src"))  # ajusta según tu estructura
def convert_to_str(X):
    return X.astype(str)
__main__.convert_to_str = convert_to_str
# Importa la función antes de cargar el modelo



import pickle
import joblib
os.chdir("../models")
#saco las pipelines /modelos


modelo_timely=joblib.load("modelo_timely_tree_def.pkl")

import dill



with open("modelo_pipe_dispute_knn.pkl", "rb") as f:
    modelo_dispute = dill.load(f)


#necesito esta funcion para que fincione porque no me dejaba exportarlo de otra forma


"""modelo_dispute=joblib.load("modelo_pipe_dispute_knn_def.pkl")"""

# Aplicacion
app=FastAPI()
#GET
@app.get("/")
async def root():
    return {"servidor": "Minority Report bancario","version": "v01"}

#GET
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "id": q}

@app.get("/predict_timely{Issue}_{Subissue}_{Companyresponse}_{Product}_{Subproduct}_{State}")
def predict_timely (    

    
    Issue: int,
    Companyresponse: int,
    Product: int=7,
    Subproduct: int=39,
    Subissue: int = 39,
    State: int = 52):
    
    #State por defecto Unknown
    #Subproduct por defecto Unknown or 
    #Subissue por defecto Unknown or 

    #Product por defecto other financia services

    #Yes=1, No= 0


    

    features=pd.DataFrame(
        {
            "Product":[Product],
            "Sub-product": [Subproduct],	
            "Issue":[Issue],	
            "Sub-issue":[Subissue],	
            "State":[State],	
            "Company response":[Companyresponse],
            

}
    )
    
    pred=modelo_timely.predict(features)[0]

    
    return {"response01": int(pred)}




@app.get("/predict_dispute{Issue}_{Subissue}_{Companyresponse}_{Product}_{Subproduct}_{State}_{zip}")
def predict_dispute (
    Product: int,
    Subproduct: int,
    Issue: int,
    Companyresponse: int,
    timely: int=None,
    Subissue: int = 39,
    State: int = 52, 
    zip:int=000
):
    """State por defecto Unknown
    Subissue por defecto Unknown or 
    Yes=2, No= 0, duda =1"""
    
    
    
    if timely is None:
        timely = int(predict_timely(Issue=Issue,Subissue=Subissue , Companyresponse=Companyresponse, Product=Product, Subproduct=Subproduct , State=State )["response01"])
    print(timely)


    
    features=pd.DataFrame({

            "Product":[Product],
            "Sub-product": [Subproduct],	
            "Issue":[Issue],	
            "Sub-issue":[Subissue],	
            "State":[State],	
            "Company response":[Companyresponse],
            "Timely response?": [timely],
            "ZIP code":[zip]

})
    


    pred=modelo_dispute.predict(features)[0]
    prob=modelo_dispute.predict_proba(features)[0]

    return {"response": pred,"probability":prob.tolist() }