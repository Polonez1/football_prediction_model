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

    home_xG: float
    away_xG: float
    elo_diff: int
    place_elo_home: int
    place_elo_away: int
    home_form: float
    away_form: float


# uvicorn main:app --reload
# or
# python -m uvicorn main:app --reload
app = FastAPI()


@app.on_event("startup")
async def load_model():
    global model
    model = joblib.load("model.joblib")


@app.post("/predict")
def predict(pos: DataToPredict):
    data = pd.DataFrame([dict(pos)])
    prediction = model.predict(data)
    return {"prediction": prediction.tolist()}
