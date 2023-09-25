import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder


class ResultTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None):
        XX = (
            X.pipe(self._add_result)
            .pipe(self._transform_date)
            .pipe(self._transform_formation)
        )

        return XX

    def _add_result(self, df: pd.DataFrame):
        df["home_result"] = df["result"].str.partition(" :")[0].astype("int")
        df["away_result"] = df["result"].str.partition(": ")[2].astype("int")

        df = df.assign(
            result_final=lambda x: np.where(
                x["home_result"] > x["away_result"],
                1,
                np.where(x["home_result"] < x["away_result"], 2, 0),
            )
        )

        return df

    def _transform_date(self, df: pd.DataFrame):
        df["date"] = pd.to_datetime(df["date"], format="%a, %d-%b-%y").dt.strftime(
            "%Y-%m-%d"
        )

        return df

    def _transform_formation(self, df: pd.DataFrame):
        df["home_formation"] = df["home_formation"].str.replace("-", "").astype("int")
        df["away_formation"] = df["away_formation"].str.replace("-", "").astype("int")

        return df


class CustomEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
        self.encoder = OrdinalEncoder()

    def fit(self, X, y=None):
        self.encoder.fit(X[self.columns])
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_encoded = self.encoder.transform(X[self.columns])
        X_copy[self.columns] = X_encoded
        return X_copy


def create_pipeline():
    pipeline = make_pipeline(ResultTransformer())

    return pipeline


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    pipeline = create_pipeline()
    transformed_data = pipeline.fit_transform(df)

    return transformed_data
