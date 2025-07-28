import requests
import pandas as pd
import numpy as np
import holidays
from sklearn.preprocessing import LabelEncoder


us_states = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    'District of Columbia': "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}
def get_zip_info(zip_code):
    """This function takes a ZIP code and returns the corresponding state abbreviation"""
    try:
        url = f"https://api.zippopotam.us/us/{int(zip_code)}"
        response = requests.get(url)
        if response.status_code == 200:
            return us_states[response.json()["places"][0]["state"]]
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"



def preprocesing_function(df_not):
    """ this function is used to preprocess the data"""
    df=df_not.copy()

    df["ZIP code"]=df["ZIP code"].astype("Int64")
    df["Issue"].fillna("Unknown or not specified", inplace=True) 
    df["Sub-issue"].fillna("Unknown or not specified", inplace=True)
    df["Sub-product"].fillna("Unknown or not specified", inplace=True)
    df["ZIP code"].fillna(0, inplace=True)
    null_state_rows = df[df["State"].isnull()]

    for idx in null_state_rows.index:
        zip_code = df.loc[idx, "ZIP code"]
        state = get_zip_info(zip_code)
        df.loc[idx, "State"] = state
    df["Date received"] = pd.to_datetime(df["Date received"], format="%Y-%m-%d")
    df["Date sent to company"] = pd.to_datetime(df["Date received"], format="%Y-%m-%d")

    product_encoder = LabelEncoder()

    df['Product'] = product_encoder.fit_transform(df['Product'] )
    df['Sub-product']=df['Sub-product'].fillna("not specified")
    sub_product_encoder = LabelEncoder()
    df['Sub-product']=df['Sub-product'].fillna("not specified")

    df['Sub-product'] = sub_product_encoder.fit_transform(df['Sub-product'] )
    State_enc = LabelEncoder()
    df['State'] = State_enc.fit_transform(df['State'] )
    Response_enc = LabelEncoder()
    df['Company response'] = Response_enc.fit_transform(df['Company response'] )
    Time_enco = LabelEncoder()
    df['Timely response?'] = Time_enco.fit_transform(df['Timely response?'] )
    df["weekday"]=df["Date received"].dt.weekday
    us_holidays = holidays.US()
    df["holiday"]= df["Date received"].isin(us_holidays)
    Company_enco = LabelEncoder()
    df['Company'] = Company_enco.fit_transform(df['Company'] )
    df["Consumer disputed?"].fillna("Unknown or not specified", inplace=True)
    
    return df
