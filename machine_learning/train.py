import sys
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split

sys.path.append("./machine_learning/")

import data_processing_xy
import transformer


def train_model():
    df = pd.read_excel("./data/downloaded_data/matches.xlsx")

    return df


if "__main__" == __name__:
    df = train_model()
    dft = transformer.transform_data(df)
    X, y = data_processing_xy.split_X_y(dft)
    tts = train_test_split(X, y, stratify=y, test_size=0.3)

    X_train, X_test, y_train, y_test = tts

    print(X_train.head())
