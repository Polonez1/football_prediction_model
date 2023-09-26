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
    home_Goals: int
    away_Goals: int
    home_Assists: int
    away_Assists: int
    home_Average_Ratings: float
    away_Average_Ratings: float
    home_Average_Age: float
    away_Average_Age: float
    home_Average_Height: float
    away_Average_Height: float
    home_Shots_pg: float
    away_Shots_pg: float
    home_Aerial_Duel_Success: int
    away_Aerial_Duel_Success: int
    home_Dribbles_pg: float
    away_Dribbles_pg: float
    home_Tackles_pg: float
    away_Tackles_pg: float
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


@app.on_event("startup")
async def load_data():
    global fixtures
    fixtures = pd.read_json("fixtures.json")


@app.get("/static_table")
def get_static_table():
    return fixtures


@app.get("/static_table/match_name={match_name}")
def get_team_by_id(match_name: str):
    for item in fixtures:
        if item == match_name:
            return fixtures[item]
    return {"message": "Team not found"}


@app.post("/predict")
def predict(post: DataToPredict):
    data = pd.DataFrame([dict(post)])
    prediction = model.predict(data)
    return {"prediction": prediction.tolist()}
