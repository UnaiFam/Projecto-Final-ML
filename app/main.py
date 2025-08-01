from typing import Union
from fastapi import FastAPI
import pandas as pd
"""Projecto-Final-ML/app/fastapi dev main.py"""

"""    server   Server started at 
    server   Documentation at 
"""
""" parar ctrl C"""

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

@app.get("/predict")
def predict(sepal_length:float):
    #arriba features

    """predict""" 
    
  #pasa features a pd dataframe
   # le da a predirs"""
    features=pd.DataFrame({"sepal lengcm":[sepal_length]
    })
    pred=model.predict(features)[0]
    return {"y": pred}

