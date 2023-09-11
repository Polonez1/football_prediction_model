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
        self.home_avg = X["home_result"].mean()  # 1.44
        self.away_avg = X["away_result"].mean()  # 1.22
        self.overall_avg = self.home_avg + self.away_avg  # 2.9

        return self

    def transform(self, X: pd.DataFrame, y=None):
        X1 = self._add_elo_xG(X)
        X2 = self._add_elo_diff(X1)
        X3 = self._correct_xG(X2)
        X4 = self._xG_coef(X3)
        X5 = self._xG_multiple_coef(X4)

        return X5

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

    def _calculate_elo_diff_coef(self, elo1, elo2):
        if elo1 <= elo2:
            if elo1 > elo2 - 50:
                fcoef = 1
            elif elo1 > elo2 - 100:
                fcoef = 0.90
            elif elo1 > elo2 - 200:
                fcoef = 0.8
            else:
                fcoef = 0.6
        else:
            if elo1 <= elo2 + 50:
                scoef = 1
            elif elo1 <= elo2 + 100:
                scoef = 1.1
            elif elo1 <= elo2 + 200:
                scoef = 1.2
            else:
                scoef = 1.4

        return fcoef if elo1 <= elo2 else scoef

    def _xG_coef(self, df: pd.DataFrame):
        df["home_coef"] = df.apply(
            lambda row: self._calculate_elo_diff_coef(row["home_elo"], row["away_elo"]),
            axis=1,
        )
        df["away_coef"] = df.apply(
            lambda row: self._calculate_elo_diff_coef(row["away_elo"], row["home_elo"]),
            axis=1,
        )

        return df

    def _xG_multiple_coef(self, df: pd.DataFrame):
        df["home_xG"] = df["home_xG"] * df["home_coef"]
        df["away_xG"] = df["away_xG"] * df["away_coef"]

        return df

    def _correct_xG(self, df: pd.DataFrame):
        df["stde_home"] = self.home_avg - df["home_xG"]
        df["stde_away"] = self.home_avg - df["away_xG"]

        stde_avg_home = df["stde_home"].mean()
        stde_avg_away = df["stde_away"].mean()

        df["home_xG"] = df["home_xG"] + stde_avg_home
        df["away_xG"] = df["away_xG"] + stde_avg_away

        return df

    def _add_elo_diff(self, df: pd.DataFrame, y=None):
        df["elo_diff"] = df["home_elo"] - df["away_elo"]
        return df


def create_pipeline():
    col_transformer = ColumnTransformer(
        transformers=[
            ("result", make_pipeline(OrdinalEncoder()), ["result"]),
        ],
    )

    pipeline = make_pipeline(ResultTransformer(), col_transformer)

    return pipeline


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
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
            "home_prb",
            "draw_prb",
            "away_prb",
            "home_result",
            "away_result",
        ]
    ]
    dft = transform_data(df)

    print(dft)
