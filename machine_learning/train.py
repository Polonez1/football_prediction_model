import sys
import pandas as pd
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib

# from ray import tune
# from ray.tune.search.hyperopt import HyperOptSearch
import ray

sys.path.append("./machine_learning/")

import data_processing_xy
import transformer
import ml_config
import rfc_model

import transformer_wsc


def train_model():
    df = pd.read_excel(ml_config.DATA_PATH_BY_ELO)
    dft = transformer.transform_data(df)
    X, y = data_processing_xy.split_X_y(dft)
    tts = train_test_split(X, y, stratify=y, test_size=0.3)

    X_train, X_test, y_train, y_test = tts
    #
    rfc = rfc_model.create_rfc_model(params=ml_config.rfc_params)
    rfc.fit(X_train, y_train)
    sc = rfc.score(X_test, y_test)
    model = rfc_model.shap_explainer(rfc, X_test=X_test)

    # scores = cross_val_score(rfc, X_test, y_test, cv=3)
    # score = rfc.score(X_test, y_test)

    return X_train


def train_model2():
    df = pd.read_excel(ml_config.DATA_PATH_BY_STATS)
    df = transformer_wsc.transform_data(df)
    X, y = data_processing_xy.split_X_y_wsc(df)
    tts = train_test_split(X, y, stratify=y, test_size=0.3)

    X_train, X_test, y_train, y_test = tts
    rfc = rfc_model.create_rfc_model(params=ml_config.rfc_params)
    rfc.fit(X_train, y_train)
    # sc = rfc.score(X_test, y_test)
    # rfc_model.shap_explainer(rfc, X_test=X_test)
    # scores = cross_val_score(rfc, X_test, y_test, cv=3)

    return df


if "__main__" == __name__:
    model = train_model2()
    print(model.loc[model["result_final"] == 0])
    # print(model["date"].head(10))
    # joblib.dump(model, ".\deployment\model.joblib")
