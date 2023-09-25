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

COL_TO_XX = [
    "home_Goals",
    "away_Goals",
    "home_Assists",
    "away_Assists",
    "home_Average_Ratings",
    "away_Average_Ratings",
    "home_Average_Age",
    "away_Average_Age",
    "home_Average_Height",
    "away_Average_Height",
    "home_Shots_pg",
    "away_Shots_pg",
    "home_Aerial_Duel_Success",
    "away_Aerial_Duel_Success",
    "home_Dribbles_pg",
    "away_Dribbles_pg",
    "home_Tackles_pg",
    "away_Tackles_pg",
    "home_formation",
    "away_formation",
]


COL_TO_Y = ["result_final"]


DATA_PATH_BY_ELO = "./data/downloaded_data/matches.xlsx"
DATA_PATH_BY_STATS = "./data/downloaded_data/EPL_22_23.xlsx"

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
