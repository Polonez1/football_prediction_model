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
]
COL_TO_Y = ["result_final"]


DATA_PATH = "./data/downloaded_data/matches1.xlsx"


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
    "n_estimators": [1, 5, 10, 25, 50, 75, 100],
    "max_depth": [None, 5, 10, 15, 20, 25, 50],
    "criterion": ["gini"],
    "min_samples_split": [1, 5, 10, 15, 20],
    "max_features": ["sqrt"],
    # "bootstrap": [True, False],
    # "oob_score": [True, False],
}
