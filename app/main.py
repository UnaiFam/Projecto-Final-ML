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
fastapi dev main.py

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


modelo_timely=joblib.load("modelo_timely_tree_sin_comp.pkl")
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
@app.get("/predict_timely{Issue}_{Subissue}_{Product}_{Subproduct}_{State}")


def predict_timely (    
    Issue: int=86,
    Product: int=7,
    Subproduct: int=39,
    Subissue: int = 39,
    State: int = 52):
    
    """
    Los codigos numericos estan en docs ID.md, en IDipynb y tambien en los encoder en la carpeta src tool_preprocess.py
    calcula el si se respondera a tiempo 
    Thershold de yes/no 0.5
    Valores por defecto:
    Product: Other financial service
    Subproduct Unknown or not specified 
    Issue: Unknown or not specified
    Subissue Unknown or not specified
    State Unknown or not specified

    Devuelve             
    "response":Yes/No
            "response01": 1/0
            "prob": %
    
    """


    # cogo los features y los pongo en df
    features=pd.DataFrame(
        {
            "Product":[Product],
            "Sub-product": [Subproduct],	
            "Issue":[Issue],	
            "Sub-issue":[Subissue],	
            "State":[State],	
        }
    )
    #predigo el df

    pred=(float(modelo_timely.predict_proba(features)[:,1])>=0.5)
    prob= float(modelo_timely.predict_proba(features)[:,1])

    # paso para yes no
    if int(pred)==1:
        response="Yes"
    else:
        response="No"

    return {"response01": int(pred), "timeprob":prob, "response":response
            }


    

@app.get("/predict_dispute{Product}_{Subproduct}_{Issue}_{Subissue}_{State}_{Company}_{Companyresponse}_{timely}_{weekday}")
def predict_dispute (
    timely,
    Issue:int, 
    Company:int,
    Companyresponse:int, 
    weekday:int,
    Product: int=7,
    Subproduct:int=39,
    Subissue:int=39, 
    State:int=52,
    ):

    """    
    Los codigos numericos estan en docs ID.md, en IDipynb y tambien en los encoder en la carpeta src tool_preprocess.py
    Funcion que predice si el cliente disputara o no.

    Product: Other financial service
    Subproduct: Unknown or not specified 
    Issue: Unknown or not specified
    Subissue: Unknown or not specified
    State: Unknown or not specified
    timely: response None
    
    Thershold de yes/no 0.5
    Si timely response es none lo predice y da los reslutado
    Devuelve:
        "response":Yes/No
        "response01": 1/0
        "prob": %
    Si timely response es none lo predice pero no devolvera los resultados, para consultarlos hacerlo por separado
    
    """

    if timely == None:
        timely_res = (predict_timely(Issue=Issue,Subissue=Subissue , Product=Product, Subproduct=Subproduct , State=State ))
        timely=timely_res["response"]
    else:
        timely_res='Not calculated'

    
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
    
    features["Timely response?"].replace([1,0], ["Yes", "No"], inplace=True)
    
    features["Product"] = product_encoder.inverse_transform(pd.DataFrame(features["Product"]))
    features["Sub-product"] = sub_product_encoder.inverse_transform(pd.DataFrame(features["Sub-product"]))
    features["Issue"] = Issue_enc.inverse_transform(pd.DataFrame(features["Issue"]))
    features["Sub-issue"] = sub_Issue_enc.inverse_transform(pd.DataFrame(features["Sub-issue"]))
    features["Company"] = Company_enc.inverse_transform(pd.DataFrame(features["Company"]))
    features["State"] = State_enc.inverse_transform(pd.DataFrame(features["State"]))
    features["Company response"] = Company_response_enc.inverse_transform(pd.DataFrame(features["Company response"]))
    features["weekday"]=week_enc.inverse_transform(pd.DataFrame(features["weekday"]))

    features_pro=preprocesador.transform(features)

    pred=(modelo_dispute.predict(features_pro) >= 0.5).astype(int)
    if pred== 1:
        res="Yes"
    else :
        res="No"
    prob=modelo_dispute.predict(features_pro)

    return {"response":res, "response01": int(pred), "prob": float(prob), "timely":timely_res}