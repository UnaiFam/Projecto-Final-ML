import gradio as gr
import os

import pandas as pd
import pickle
import os
import sys
import __main__
import os
import joblib


"""


python app_render_timely.py



"""

base_dir = os.path.dirname(__file__)             # .../app
src_dir = os.path.join(base_dir, "..", "src")    # .../src
sys.path.append(os.path.abspath(src_dir))

# los saco porque el modelo dispute necesita decodificarlo
from tool_preprocess import product_encoder,sub_product_encoder, Issue_enc, sub_Issue_enc, State_enc, Company_response_enc, Company_enc, week_enc


base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "..", "src", "preprocesador_red.pkl")

with open(model_path, "rb") as f:
    preprocesador = joblib.load(f)



#saco las pipelines /modelos
model_path = os.path.join(base_dir,"..", "models", "modelo_timely_tree_sin_comp_def.pkl")

with open(model_path, "rb") as f:
    modelo_timely = joblib.load(f)



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