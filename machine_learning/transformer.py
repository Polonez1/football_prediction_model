import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder


class ResultTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None):
        return self._add_result(X)

    def _add_result(self, df: pd.DataFrame):
        df = df.assign(
            result=lambda x: np.where(
                x["home_result"] > x["away_result"],
                "home_win",
                np.where(x["home_result"] < x["away_result"], "away_win", "draw"),
            )
        )

        return df


class EloTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, elo_factor=1000):
        self.home_avg = None
        self.away_avg = None
        self.overall_avg = None
        self.elo_factor = elo_factor

    def fit(self, X: pd.DataFrame, y=None):
        self.home_avg = X["home_result"].mean()
        self.away_avg = X["away_result"].mean()
        self.overall_avg = self.home_avg + self.away_avg

        return self

    def transform(self, X: pd.DataFrame, y=None):
        return self._add_elo_xG(X)

    def _calc_elo_xG(self, elo1, elo2):
        xG_coef = 1 / (10 ** ((elo1 - elo2) / self.elo_factor) + 1)

        return xG_coef

    def _add_elo_xG(self, df: pd.DataFrame):
        df = df.assign(
            home_xG=lambda x: self._calc_elo_xG(elo1=x["away_elo"], elo2=x["home_elo"])
            * self.overall_avg
        )
        df = df.assign(
            away_xG=lambda x: self._calc_elo_xG(elo1=x["home_elo"], elo2=x["away_elo"])
            * self.overall_avg
        )

        return df
        # df = df.assign()


def create_pipeline():
    col_transformer = ColumnTransformer(
        transformers=[
            ("result", make_pipeline(OrdinalEncoder()), ["result"]),
        ],
    )

    pipeline = make_pipeline(ResultTransformer(), col_transformer)

    return pipeline


def transform_data(df: pd.DataFrame):
    pipeline = create_pipeline()
    transformed_data = pipeline.fit_transform(df)
    transformed_result_series = pd.Series(transformed_data[:, 0], name="result_final")
    df["result_final"] = transformed_result_series

    elo_transf = EloTransformer(elo_factor=400)
    dft = elo_transf.fit_transform(df)

    return dft


# 0 - away win, 1 - draw, 2 - home win

if "__main__" == __name__:
    df = pd.read_excel("./data/downloaded_data/matches.xlsx")
    df = df[
        [
            "home_team",
            "home_elo",
            "away_team",
            "away_elo",
            "home_result",
            "away_result",
        ]
    ]
    dft = transform_data(df)

    # dff = tr.fit_transform(df)

    print(dft.head(20))
