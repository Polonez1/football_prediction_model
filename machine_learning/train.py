import sys
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score


# from ray import tune
# from ray.tune.search.hyperopt import HyperOptSearch

sys.path.append("./machine_learning/")

import data_processing_xy
import transformer
import ml_config
import rfc_model


def train_model():
    df = pd.read_excel(ml_config.DATA_PATH)
    dft = transformer.transform_data(df)
    X, y = data_processing_xy.split_X_y(dft)
    tts = train_test_split(X, y, stratify=y, test_size=0.3)
    #
    X_train, X_test, y_train, y_test = tts

    rfc = rfc_model.create_rfc_model(params=ml_config.rfc_params)

    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)
    scores = cross_val_score(rfc, X_test, y_test, cv=5)

    # score = rfc.score(X_test, y_test)
    return scores


if "__main__" == __name__:
    res = train_model()
    print(res)
