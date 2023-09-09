import pandas as pd

import sys

sys.path.append("./machine_learning/")

import ml_config


def split_X_y(df: pd.DataFrame) -> pd.DataFrame:
    X = df[ml_config.COL_TO_X]
    y = df[ml_config.COL_TO_Y]
    y = y.to_numpy().ravel()

    return X, y
