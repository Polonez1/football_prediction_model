import requests
import pandas as pd
import json

import sys

sys.path.append("./scraping/")
sys.path.append("./machine_learning/")


import transformer_wsc
import ml_config


def show_fixtures():
    fixtures_df = requests.get(f"http://127.0.0.1:8000/static_table")
    fixtures = fixtures_df.json()

    for key in fixtures:
        name = f"\x1b[32m {key} \x1b[0m"
        date = fixtures[key]["date"]
        kick_off = fixtures[key]["Kick off"]
        print(f"{name}: {date} \x1b[34m {kick_off} \x1b[0m")


def get_fixtures_match(match_name: str):
    match_name = requests.get(
        f"http://127.0.0.1:8000/static_table/match_name={match_name}"
    )

    match_name = [match_name.json()]
    df = pd.DataFrame(match_name)
    dff = transformer_wsc.transform_predict_dat(df)
    data_to_predict: pd.DataFrame = dff[ml_config.COL_TO_XX]
    json_data = data_to_predict.to_json(orient="records")

    return json.loads(json_data)[0]


def get_prediction(json_data=0):
    data = {
        "home_Goals": 4,
        "away_Goals": 4,
        "home_Assists": 3,
        "away_Assists": 3,
        "home_Average_Ratings": 6.5,
        "away_Average_Ratings": 6.8,
        "home_Average_Age": 25.4,
        "away_Average_Age": 24.6,
        "home_Average_Height": 183.8,
        "away_Average_Height": 182.7,
        "home_Shots_pg": 1.3,
        "away_Shots_pg": 1.3,
        "home_Aerial_Duel_Success": 39,
        "away_Aerial_Duel_Success": 66,
        "home_Dribbles_pg": 0.9,
        "away_Dribbles_pg": 0.9,
        "home_Tackles_pg": 1.3,
        "away_Tackles_pg": 1.1,
        "home_formation": 4231,
        "away_formation": 352,
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)
    # print(response.json())

    return response.json()


if "__main__" == __name__:
    # json_data = get_fixtures_match(match_name="Bournemouth-Chelsea")
    score = get_prediction()
    print(score)
    # print(json_data)

    # print(json_data)
