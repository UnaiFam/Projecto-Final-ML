import gradio as gr
import os
os.chdir("../src")
from tool_preprocess import State_enc, product_encoder, sub_Issue_enc, sub_product_encoder,  Issue_enc, Company_response_enc, Time_enco, preprocesing_function_paraforest

import pandas as pd
import pickle
import os

import os
import joblib

os.chdir("../models")
with open('modelo_timely_tree_sin_comp_def.pkl', 'rb') as f:
    modelo_timely = pickle.load(f)


import pickle
import joblib
os.chdir("../models")
#saco las pipelines /modelos


modelo_timely=joblib.load("modelo_timely_tree_sin_comp_def.pkl")
def predict_timely (    
    Product:str,
    Subproduct:str,
    Issue:str,
    Subissue:str,
    State:str,
    ):
    
    #State por defecto Unknown or not specified
    #Subproduct por defecto Unknown or not specified
    #Subissue por defecto Unknown or not specified
    #Product por defecto other financial services

    #Yes=1, No= 0


    
# 
    features=pd.DataFrame({"Product":[Product],
                           "Sub-product": [Subproduct],	
            "Issue":[Issue],	
            "Sub-issue":[Subissue],	
            "State":[State],	
            })

    display(features)
    features["Product"] = product_encoder.transform(features["Product"])
    features["Sub-product"] = sub_product_encoder.transform(features["Sub-product"])
    features["Issue"] = Issue_enc.transform(features["Issue"])
    features["Sub-issue"] = sub_Issue_enc.transform(features["Sub-issue"])
    features["State"] = State_enc.transform(features["State"])
    
    
    display(features)
    pred=(float(modelo_timely.predict_proba(features)[:,1])>=0.5)
    prob= float(modelo_timely.predict_proba(features)[:,1])

    if int(pred)==1:
        response="Yes"
    else:
        response="No"

    return {"response01": int(pred), "timeprob":prob, "response":response
            }

iface = gr.Interface(
    #meto la fucncos
    fn=predict_timely,
    inputs=[# meto el front
        gr.Dropdown(choices=product_encoder.classes_.tolist(), value='Unknown or not specified', label="Product"),
        gr.Dropdown(choices=sub_product_encoder.classes_.tolist(), value='Unknown or not specified', label="Sub-product"),
        gr.Dropdown(choices=Issue_enc.classes_.tolist(), value='Unknown or not specified', label="Issue"),
        gr.Dropdown(choices=sub_Issue_enc.classes_.tolist(), value='Unknown or not specified', label="Sub-issue"),
        gr.Dropdown(choices=State_enc.classes_.tolist(), value='Unknown or not specified', label="State"),
        gr.Dropdown(choices=Company_response_enc.classes_.tolist(), value='Unknown or not specified', label="Company response"),
    ],
    #sale json
    outputs="json",
    title="Predicción Timely",
    description="Introduce los parámetros para obtener la predicción."
)
if __name__ == "__main__":
    iface.launch()