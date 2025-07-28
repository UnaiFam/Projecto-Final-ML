import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


import requests
import pandas as pd
import numpy as np
import holidays
from sklearn.preprocessing import LabelEncoder


# poner los encoder para que seimpre sea el mismo 

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
def get_zip_info(zip_code: str) -> str:
    """This function takes a ZIP code and returns the corresponding state abbreviation"""
    try:
        url = f"https://api.zippopotam.us/us/{int(zip_code)}"
        response = requests.get(url) #intonto entrar eb la api
        if response.status_code == 200: #si me deja que me devieva el estado y luego pongo las iniciales del dict de arriba
            return us_states[response.json()["places"][0]["state"]]
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"

product_encoder = LabelEncoder()
product_encoder.fit(pd.DataFrame(['Debt collection', 'Mortgage', 'Credit card', 'Consumer loan',
       'Bank account or service', 'Payday loan', 'Credit reporting',
       'Money transfers', 'Student loan', 'Prepaid card',
       'Other financial service']))

sub_product_encoder = LabelEncoder()
sub_product_encoder.fit(pd.DataFrame(['Unknown or not specified', 'Medical', 'FHA mortgage',
       'Non-federal student loan', 'Payday loan', 'Installment loan',
       'Other (phone, health club, etc.)', 'Other bank product/service',
       'Vehicle loan', 'Checking account', 'Credit card',
       'Conventional adjustable mortgage (ARM)',
       'Conventional fixed mortgage', 'Domestic (US) money transfer',
       'Personal line of credit', '(CD) Certificate of deposit',
       'Vehicle lease', 'Mortgage', 'Savings account',
       'International money transfer',
       'Home equity loan or line of credit', 'Auto', 'Other mortgage',
       'Cashing a check without an account', 'Federal student loan',
       'Pawn loan', 'VA mortgage', 'General purpose card',
       'Other special purpose card', 'Gift or merchant card',
       'Check cashing', 'Reverse mortgage', 'Mobile wallet', 'Title loan',
       'Debt settlement', 'Money order', 'Payroll card',
       'Government benefit payment card', 'Refund anticipation check',
       'ID prepaid card', "Traveler's/Cashier's checks",
       'Foreign currency exchange', 'Credit repair']))

State_enc = LabelEncoder()
State_enc.fit(pd.DataFrame(['TX', 'MA', 'CA', 'OH', 'NJ', 'ND', 'RI', 'CO', 'UT', 'AL', 'PA',
       'NY', 'NC', 'GA', 'IL', 'WI', 'MI', 'FL', 'CT', 'OR', 'VA', 'WA',
       'TN', 'MD', 'IA', 'KY', 'LA', 'OK', 'NE', 'KS', 'MO', 'NH', 'IN',
       'DC', 'NV', 'ME', 'NM', 'SC', 'AZ', 'AP', 'MS', 'MN', 'ID', 'HI',
       'PR', 'Unknown', 'WV', 'WY', 'AK', 'VI', 'MT', 'DE', 'AR', 'AE',
       'SD', 'GU', 'VT', 'MH', 'PW', 'AS']) )

Issue_enc = LabelEncoder()
Issue_enc.fit(pd.DataFrame(['Communication tactics', "Cont'd attempts collect debt not owed",
       'Application, originator, mortgage broker', 'Other',
       'Managing the loan or lease',
       'Taking/threatening an illegal action',
       'False statements or representation', 'Deposits and withdrawals',
       "Can't contact lender", 'Disclosure verification of debt',
       'Loan modification,collection,foreclosure',
       'Improper contact or sharing of info',
       'Problems when you are unable to pay',
       'Account opening, closing, or management',
       'Incorrect information on credit report',
       'Loan servicing, payments, escrow account',
       'Other transaction issues',
       "Credit reporting company's investigation", 'Delinquent account',
       'Late fee', 'Taking out the loan or lease',
       'Credit decision / Underwriting', 'Managing the line of credit',
       "Can't stop charges to bank account",
       "Charged fees or interest I didn't expect",
       'Improper use of my credit report', 'Using a debit or ATM card',
       'Billing statement', 'Problems caused by my funds being low',
       "Can't repay my loan", 'Making/receiving payments, sending money',
       'Charged bank acct wrong day or amt',
       "Received a loan I didn't apply for", 'Other service issues',
       'Money was not available when promised',
       'Unable to get credit report/credit score',
       'Shopping for a loan or lease', 'Fraud or scam',
       'Payment to acct not credited',
       'Credit monitoring or identity protection', 'Getting a loan',
       'Cash advance fee', 'APR or interest rate',
       'Settlement process and costs', 'Closing/Cancelling account',
       'Billing disputes', 'Identity theft / Fraud / Embezzlement',
       'Bankruptcy', 'Credit card protection / Debt protection',
       'Dealing with my lender or servicer', 'Payoff process',
       'Credit determination', 'Customer service / Customer relations',
       'Unsolicited issuance of credit card',
       'Unauthorized transactions/trans. issues', 'Privacy',
       'Transaction issue', 'Application processing delay',
       'Balance transfer fee', 'Credit line increase/decrease',
       'Disclosures', 'Wrong amount charged or received',
       'Balance transfer', 'Advertising and marketing',
       'Applied for loan/did not receive money',
       'Managing, opening, or closing account', 'Rewards',
       'Account terms and changes', 'Overlimit fee', 'Cash advance',
       'Other fee', 'Forbearance / Workout plans',
       'Lost or stolen money order',
       'Incorrect/missing disclosures or info',
       'Customer service/Customer relations',
       'Overdraft, savings or rewards features', 'Adding money', 'Fees',
       'Lost or stolen check', 'Sale of account', 'Convenience checks',
       'Incorrect exchange rate', 'Arbitration',
       'Lender repossessed or sold the vehicle', 'Unexpected/Other fees',
       'Unknown or not specified', 'Lender damaged or destroyed vehicle',
       'Shopping for a line of credit',
       'Advertising, marketing or disclosures', 'Excessive fees']) )


sub_Issue_enc = LabelEncoder()
sub_Issue_enc.fit(pd.DataFrame(['Frequent or repeated calls', 'Debt is not mine',
       'Unknown or not specified', 'Debt resulted from identity theft',
       'Called after sent written cease of comm', 'Debt was paid',
       'Threatened arrest/jail if do not pay',
       'Impersonated an attorney or official',
       'Not given enough info to verify debt',
       'Attempted to collect wrong amount',
       'Used obscene/profane/abusive language',
       'Right to dispute notice not received',
       'Contacted employer after asked not to',
       'Contacted me after I asked not to',
       'Threatened to take legal action', 'Account terms',
       'Debt was discharged in bankruptcy', 'Account status',
       'Threatened to sue on too old debt', 'Investigation took too long',
       'Personal information', 'Called outside of 8am-9pm',
       'Public record', 'Talked to a third party about my debt',
       'Report improperly shared by CRC', 'Information is not mine',
       'Problem with statement of dispute',
       'Problem getting my free annual report',
       'Problem getting report or credit score',
       'Reinserted previously deleted info',
       'Report shared with employer w/o consent', 'Billing dispute',
       'No notice of investigation status/result',
       'Problem with fraud alerts', 'Inadequate help over the phone',
       'Indicated committed crime not paying',
       'Problem cancelling or closing account',
       'Not disclosed as an attempt to collect',
       'Receiving unwanted marketing/advertising',
       'Account terms and changes',
       'Sued w/o proper notification of suit',
       'Seized/Attempted to seize property',
       'Contacted me instead of my attorney',
       "Indicated shouldn't respond to lawsuit",
       "Sued where didn't live/sign for debt",
       'Attempted to/Collected exempt funds',
       'Received marketing offer after opted out']) )





Time_enco = LabelEncoder()
Time_enco.fit(pd.DataFrame(['Yes', 'No']) )



companies= open("company_names.txt", "r")


Company_enc = LabelEncoder()
Company_enc.fit(pd.DataFrame(companies.read().split(";")))



Dispute_enco = LabelEncoder()
Dispute_enco.fit(pd.DataFrame(["Unknown or not specified", 'Yes', 'No']))


def preprocesing_function_paraforest(df_not: pd.DataFrame) -> pd.DataFrame:
    """ this function is used to preprocess the data uing label encoding"""
    df=df_not.copy()
    #lo copio
    df["ZIP code"]=df["ZIP code"].astype(np.int64)
    # lo paso a int para el zip code
    df["Issue"].fillna("Unknown or not specified", inplace=True) 
    df["Sub-issue"].fillna("Unknown or not specified", inplace=True)
    df["Sub-product"].fillna("Unknown or not specified", inplace=True)
    df["ZIP code"].fillna(0, inplace=True)
    df["ZIP code"].fillna(0, inplace=True)
    df["Consumer disputed?"].fillna("Unknown or not specified", inplace=True)

    # relleno los valores nulos de las columnas con un valor que no se va a usar
    null_state_rows = df[df["State"].isnull()]
    # saco las filas que tienen el estado nulo

    for idx in null_state_rows.index:
        # miro en cada fila que tiene el estado nulo y saco el zip code
        zip_code = df.loc[idx, "ZIP code"]

        state = get_zip_info(zip_code)
        # llamo a la funcion que me devuelve el estado
        df.loc[idx, "State"] = state

        # cambio el tipo para sacar otras cosas por si acaso
    df["Date received"] = pd.to_datetime(df["Date received"], format="%Y-%m-%d")
    df["Date sent to company"] = pd.to_datetime(df["Date received"], format="%Y-%m-%d")

#codificadrores
# pordoductos lleno los huevcos con not specified y luego lo codifico



    df['Product']=df['Product'].fillna("Unknown or not specified")
    df['Product'] = product_encoder.transform(df['Product'] )


    df['Sub-product']=df['Sub-product'].fillna("Unknown or not specified")
    df['Sub-product'] = sub_product_encoder.transform(df['Sub-product'] )


    df['State'] = State_enc.fit_transform(df['State'] )

    df['Issue']=df['Issue'].fillna("Unknown or not specified")
    df['Issue'] = Issue_enc.transform(df['Issue'] )


    df['Sub-issue']=df['Sub-issue'].fillna("Unknown or not specified")
    df['Sub-issue'] = sub_Issue_enc.transform(df['Sub-issue'])



    df['Timely response?']=Time_enco.transform(df['Timely response?'] )




    df['Company']=Company_enc.transform(df['Company'])


    df["Consumer disputed?"].fillna("Unknown or not specified", inplace=True)
    df['Consumer disputed?']=Dispute_enco.transform(df['Consumer disputed?'] )

    
    # digo si es mfestivo o no 
    df["weekday"]=df["Date received"].dt.weekday
    us_holidays = holidays.US()
    df["holiday"]= df["Date received"].isin(us_holidays)


     #devuelve dataframe
    return df
