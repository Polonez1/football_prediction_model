import sys
import pandas as pd
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# from ray import tune
# from ray.tune.search.hyperopt import HyperOptSearch
import ray

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

    X_train, X_test, y_train, y_test = tts
    #
    rfc = rfc_model.create_rfc_model(params=ml_config.rfc_params)
    rfc.fit(X_train, y_train)
    sc = rfc.score(X_test, y_test)
    rfc_model.shap_explainer(rfc, X_test=X_test)
    scores = cross_val_score(rfc, X_test, y_test, cv=5)

    score = rfc.score(X_test, y_test)

    # clf = RandomForestClassifier()

    #
    # grid_search = GridSearchCV(
    #    estimator=clf, param_grid=ml_config.param_grid, cv=5, n_jobs=2, verbose=3
    # )
    # grid_search.fit(X_train, y_train)
    # print(grid_search.best_params_)
    # print("Best GridSearchCV Score:")
    # print(grid_search.best_score_)

    return scores


#

if "__main__" == __name__:
    res = train_model()
    print(res)
