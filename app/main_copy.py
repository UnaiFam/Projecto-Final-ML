from typing import Union
from fastapi import FastAPI
import pandas as pd
import numpy as np
import os
from datetime import datetime
import __main__
from sklearn.preprocessing import OneHotEncoder
import pickle
import joblib
from fastapi.responses import JSONResponse
# a fecha de 2/8/2025 funcionaba el docs generado, nunca he comprobado la API como tal solo los DOCS generas
"""
en anaconda prompt
code

y abrir carpeta


cd Projecto-Final-ML/app
fastapi dev main_copy.py

"""
# creo que la "IP" nunca es la misma
"""    server   Server started at 
    server   Documentation at 
"""
""" parar ctrl C"""
import sys
import os


# Importa la función antes de cargar el modelo
sys.path.append(os.path.abspath("../src"))  # ajusta según tu estructura
def convert_to_str(X):
    return X.astype(str)
__main__.convert_to_str = convert_to_str # basicamente engaña a py para esto sea de de base
os.chdir("../src")
# los saco porque el modelo dispute necesita decodificarlo
from tool_preprocess import product_encoder,sub_product_encoder, Issue_enc, sub_Issue_enc, State_enc, Company_response_enc, Company_enc, week_enc
preprocesador = joblib.load("preprocesador_red.pkl")
import pickle

os.chdir("../models")
#saco las pipelines /modelos


modelo_timely=joblib.load("modelo_timely_tree_def.pkl")
# libreria como pickle porque tuve problemas con pickle 
import dill


# saco el modelo dispute
from tensorflow import keras
modelo_dispute = keras.models.load_model("modelo_dispute_red.keras")


#necesito esta funcion para que fincione porque no me dejaba exportarlo de otra forma


"""modelo_dispute=joblib.load("modelo_pipe_dispute_knn_def.pkl")"""

# Aplicacion
app=FastAPI()
#GET
@app.get("/")
async def root():
    return {"servidor": "Minority Report bancario","version": "v02"}

#GET
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "id": q}
# wrapper para que la api haga cosas de api. 
@app.get("/predict_timely{Issue}_{Subissue}_{Companyresponse}_{Product}_{Subproduct}_{State}")
def predict_timely (    

    
    Issue: int,
    Companyresponse: int,
    Product: int=7,
    Subproduct: int=39,
    Subissue: int = 39,
    State: int = 52):
    
    #State por defecto Unknown or not specified
    #Subproduct por defecto Unknown or not specified
    #Subissue por defecto Unknown or not specified
    #Product por defecto other financial services

    #Yes=1, No= 0


    
    # cogo los features y los pongo en df
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
    #predigo el df
    pred=modelo_timely.predict(features)[0]

    #debuelve json ( con 1 y 0 porque asi no hay que cambiarlo mas adelante)
    return {"response01": int(pred)}


    

@app.get("/predict_dispute{Product}_{Subproduct}_{Issue}_{Subissue}_{State}_{Company}_{Companyresponse}_{timely}_{weekday}")
def predict_dispute (Product:int, 
    Subproduct:int, 
    Issue:int, 
    Subissue:int, 
    State:int,
    Company:int,
    Companyresponse:int, 
    timely:int, 
    weekday:int
    ):

    """
    Devuelve 'Yes' y 'No' de si el cliente disputa 
    Si no se sabe si la respuesta es a tiempo la estima

    cutoff 0.23

    """

    if timely is None:
        timely = int(predict_timely(Issue=Issue,Subissue=Subissue , Companyresponse=Companyresponse, Product=Product, Subproduct=Subproduct , State=State )["response01"])
    print(timely)

    
    features=pd.DataFrame({

            "Product":[Product],
            "Sub-product": [Subproduct],	
            "Issue":[Issue],	
            "Sub-issue":[Subissue],	
            "State":[State],	
            "weekday":[weekday],
            "Company":[Company],
            "Company response":[Companyresponse],
            "Timely response?": [timely]})
    
    features["Timely response?"] = features["Timely response?"].replace({1: "Yes", 0: "No"})
    
    features["Product"] = product_encoder.inverse_transform(pd.DataFrame(features["Product"]))
    features["Sub-product"] = sub_product_encoder.inverse_transform(pd.DataFrame(features["Sub-product"]))
    features["Issue"] = Issue_enc.inverse_transform(pd.DataFrame(features["Issue"]))
    features["Sub-issue"] = sub_Issue_enc.inverse_transform(pd.DataFrame(features["Sub-issue"]))
    features["Company"] = Company_enc.inverse_transform(pd.DataFrame(features["Company"]))
    features["State"] = State_enc.inverse_transform(pd.DataFrame(features["State"]))
    features["Company response"] = Company_response_enc.inverse_transform(pd.DataFrame(features["Company response"]))
    features["weekday"]=week_enc.inverse_transform(pd.DataFrame(features["weekday"]))

    features_pro=preprocesador.transform(features)
    pred=modelo_dispute.predict(features_pro)[0]
    # me da problemas en la api para json
    if pred>=0.235:
        return {"response": "Yes"}
    else: 
        return {"response": "No"}