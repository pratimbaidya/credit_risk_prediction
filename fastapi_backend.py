from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import joblib

from pydantic_model import UserInput

try:
    model = joblib.load('stacking_model.pkl')
    print("Stacking model loaded successfully.")
except FileNotFoundError:
    model = None
    print("Error: stacking_model.pkl not found. Make sure the file is in the same directory.")

app = FastAPI(
    title="Credit Risk Prediction API",
    version="1.0.0"
)

@app.get('/')
def home():
    return {'message': 'Welcome to The Credit Risk Prediction API'}

@app.get('/health')
def health_check():
    return{
        'status': "OK",
        'version': "1.0.0"
    }

@app.post('/predict')
def predict_default_probability(data: UserInput):

    input_df = pd.DataFrame([{
        'RevolvingUtilizationOfUnsecuredLines': data.RevolvingUtilizationOfUnsecuredLines,
        'age': data.age,
        'NumberOfTime30_59DaysPastDueNotWorse': data.NumberOfTime30_59DaysPastDueNotWorse,
        'DebtRatio': data.DebtRatio,
        'MonthlyIncome': data.MonthlyIncome,
        'NumberOfOpenCreditLinesAndLoans': data.NumberOfOpenCreditLinesAndLoans,
        'NumberOfTimes90DaysLate': data.NumberOfTimes90DaysLate,
        'NumberRealEstateLoansOrLines': data.NumberRealEstateLoansOrLines,
        'NumberOfTime60_89DaysPastDueNotWorse': data.NumberOfTime60_89DaysPastDueNotWorse,
        'NumberOfDependents': data.NumberOfDependents
    }])
    
    try:
        probability_of_default = round(model.predict_proba(input_df)[:,1].item(), 2)

        return JSONResponse(status_code=200, content={'Probability of Default ': probability_of_default})
    
    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))