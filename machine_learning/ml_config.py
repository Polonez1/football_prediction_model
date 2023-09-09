from ray import tune

COL_TO_X = [
    "home_elo",
    "away_elo",
    "home_xG",
    "away_xG",
    "home_prb",
    "draw_prb",
    "away_prb",
    # "elo_diff",
]
COL_TO_Y = ["result_final"]


DATA_PATH = "./data/downloaded_data/matches.xlsx"


rfc_params = {
    "n_estimators": 50,
    "max_depth": 3,
    "criterion": "gini",
    "min_samples_split": 20,
    # "max_features": "sqrt",
    "bootstrap": True,
}
