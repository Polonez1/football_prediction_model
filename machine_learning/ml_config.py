from ray import tune

COL_TO_X = [
    # "home_elo",
    # "away_elo",
    "home_xG",
    "away_xG",
    # "home_prb",
    # "draw_prb",
    # "away_prb",
    "elo_diff",
    "place_elo_home",
    "place_elo_away",
    "home_form",
    "away_form",
]
COL_TO_Y = ["result_final"]


DATA_PATH = "./data/downloaded_data/matches.xlsx"


rfc_params = {
    "n_estimators": 50,
    "max_depth": 5,
    "criterion": "gini",
    "min_samples_split": 20,
    "max_features": "sqrt",
    "bootstrap": True,
    "oob_score": True,
}

param_grid = {
    "n_estimators": [15, 17, 20, 23, 25, 27, 30],
    "max_depth": [None, 2, 4, 6, 8, 10],
    "criterion": ["gini"],
    "min_samples_split": [10, 15, 20, 25],
    # "max_features": ["sqrt"],
    # "bootstrap": [True, False],
    "oob_score": [True, False],
}
