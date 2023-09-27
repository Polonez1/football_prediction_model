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


def get_prediction(json_data):
    response = requests.post("http://127.0.0.1:8000/predict", json=json_data)
    # print(response.json())
    # print(response.json())

    return response.json()
    # return response.json()


def get_all_fixtures_prediction():
    fixtures_df = requests.get(f"http://127.0.0.1:8000/static_table")
    fixtures = fixtures_df.json()

    for key in fixtures:
        single_match = get_fixtures_match(match_name=key)
        pred = get_prediction(json_data=single_match)
        print(f"\x1b[32m {key} \x1b[0m: {pred}")


if "__main__" == __name__:
    # show_fixtures()

    get_all_fixtures_prediction()
