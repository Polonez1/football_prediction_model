import pandas as pd
import sys


sys.path.append("./scraping/")
sys.path.append("./data/downloaded_data/")


import scraping_elo


def _split_result(df: pd.DataFrame):
    df = df.assign(home_result=lambda x: x["Result"].str.partition("-")[0].str.strip())
    df = df.assign(away_result=lambda x: x["Result"].str.partition("-")[2].str.strip())

    return df


def download_elo_data():
    """download 5 competition ELO ratings data, season 2019-2023"""
    df = scraping_elo.create_matches_data_table()
    df = _split_result(df)

    df.to_excel("./data/downloaded_data/matches.xlsx")


if "__main__" == __name__:
    df = pd.read_excel("./data/downloaded_data/matches.xlsx")
