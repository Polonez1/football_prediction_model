import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from fastapi import FastAPI, HTTPException
from typing import List
import sys

sys.path.append("./scraping/")

import scraping_elo


class DataToPredict(BaseModel):
    """Tip model based on seaborn tip"""

    home_Goals: int
    away_Goals: int
    home_Assists: int
    away_Assists: int
    home_Average_Ratings: float
    away_Average_Ratings: float
    home_Average_Age    : float
    away_Average_Age    : float
    home_Average_Height : float
    away_Average_Height : float
    home_Shots_pg       : float
    away_Shots_pg       : float
    home_Aerial_Duel_Success: int
    away_Aerial_Duel_Success: int
    home_Dribbles_pg    : float
    away_Dribbles_pg    : float
    home_Tackles_pg     : float
    away_Tackles_pg     : float
    home_formation: int
    away_formation: int


# uvicorn main:app --reload
# or
# python -m uvicorn main:app --reload
app = FastAPI()


@app.on_event("startup")
async def load_model():
    global model
    model = joblib.load("model.joblib")
    
@app.on_event('fixtures')
async def load_data():
    global fixtures
    fixtures = pd.read_excel('epl_to_prediction.xlsx')[]
    
#global table

#get fixtures

#get fixtures list

#post list



@app.post("/predict")
def predict(pos: DataToPredict):
    data = pd.DataFrame([dict(pos)])
    prediction = model.predict(data)
    return {"prediction": prediction.tolist()}
