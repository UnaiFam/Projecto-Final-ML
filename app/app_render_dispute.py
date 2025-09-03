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


python app_render_dispute.py



"""

sys.path.append(os.path.abspath("../src"))  # ajusta según tu estructura
def convert_to_str(X):
    return X.astype(str)
__main__.convert_to_str = convert_to_str # basicamente engaña a py para esto sea de de base

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

from tensorflow import keras


model_path = os.path.join(base_dir,"..", "models", "modelo_dispute_red_def.keras")
modelo_dispute = keras.models.load_model(model_path)

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

    
    features["Product"] = product_encoder.transform(features["Product"])
    features["Sub-product"] = sub_product_encoder.transform(features["Sub-product"])
    features["Issue"] = Issue_enc.transform(features["Issue"])
    features["Sub-issue"] = sub_Issue_enc.transform(features["Sub-issue"])
    features["State"] = State_enc.transform(features["State"])
    
    
    
    pred=(float(modelo_timely.predict_proba(features)[:,1])>=0.5)
    prob= float(modelo_timely.predict_proba(features)[:,1])

    if int(pred)==1:
        response="Yes"
    else:
        response="No"

    return {"response01": int(pred), "timeprob":prob, "response":response
            }



def predict_dispute (
    Product:str, 
    Subproduct:str, 
    Issue:str, 
    Subissue:str, 
    State:str,

    Company:str,

    Companyresponse:str, 
    weekday:str,
    timely=None
    ):

    """
    Funcion que predice si el cliente disputara o no.
    Si no se da timely response lo predice y da los reslutado
    Devuelve:
        "response":Yes/No
        "response01": 1/0
        "prob": %
        timely:
            "response":Yes/No
            "response01": 1/0
            "prob": %

    """
    

    if timely == None:
        timely_res = (predict_timely(Issue=Issue,Subissue=Subissue ,  Product=Product, Subproduct=Subproduct , State=State ))
        timely=timely_res["response"]
    else:
        timely_res='Not calculated'

    print(timely_res)
    
    features=pd.DataFrame({

            "Product":[Product],
            "Sub-product": [Subproduct],	
            "Issue":[Issue],	
            "Sub-issue":[Subissue],	
            "State":[State],	
            "Company":[Company],
            "Company response":[Companyresponse],
            "Timely response?": [timely],
            
            
            
            "weekday":[weekday],})
    


    features_pro=preprocesador.transform(features)

    #pred=modelo_dispute.predict(features_pro)[0]
    pred=(modelo_dispute.predict(features_pro) >= 0.5).astype(int)
    if pred== 1:
        res="Yes"
    else :
        res="No"
    prob=modelo_dispute.predict(features_pro)

    return {"response":res, "response01": int(pred), "prob": float(prob), "timely":timely_res}



iface = gr.Interface(
    fn=predict_dispute,
    inputs=[
        gr.Dropdown(choices=product_encoder.classes_.tolist(), value='Unknown or not specified', label="Product"),
        gr.Dropdown(choices=sub_product_encoder.classes_.tolist(), value='Unknown or not specified', label="Sub-product"),
        gr.Dropdown(choices=Issue_enc.classes_.tolist(), value='Unknown or not specified', label="Issue"),
        gr.Dropdown(choices=sub_Issue_enc.classes_.tolist(), value='Unknown or not specified', label="Sub-issue"),
        
        gr.Dropdown(choices=State_enc.classes_.tolist(), value='Unknown or not specified', label="State"),
        gr.Dropdown(choices=Company_enc.classes_.tolist(), value='Unknown or not specified', label="Company"),
        gr.Dropdown(choices=Company_response_enc.classes_.tolist(), value='Unknown or not specified', label="Company response"),
        gr.Dropdown(choices=week_enc.classes_.tolist(),  label="weekday"),
        gr.Dropdown(choices=["Yes", "No", None], value=None, label="Timely response?"),
       
        
        
    ],
    outputs="json",
    title="Predicción Dispute",
    description="Introduce los parámetros para obtener la predicción."
)
if __name__ == "__main__":
    iface.launch()