import pandas as pd
import sys


sys.path.append("./scraping/")
sys.path.append("./data/downloaded_data/")


import scraping_elo


def _split_result(df: pd.DataFrame):
    df = df.assign(home_result=lambda x: x["Result"].str.partition("-")[0].str.strip())
    df = df.assign(away_result=lambda x: x["Result"].str.partition("-")[2].str.strip())

    df = df.assign(
        season_temp_1=lambda x: x["season"].str.partition("-")[0].str.strip()
    )
    df = df.assign(
        season_temp_2=lambda x: x["season"].str.partition("-")[2].str.strip()
    )

    return df


def _split_season(df: pd.DataFrame):
    df = df.assign(
        season_temp_1=lambda x: x["season"].str.partition("-")[0].str.strip()
    )
    df = df.assign(
        season_temp_2=lambda x: x["season"].str.partition("-")[2].str.strip()
    )

    df["season_temp_1"] = df["season_temp_1"].astype(int) - 1
    df["season_temp_2"] = df["season_temp_2"].astype(int) - 1

    df["season_prev"] = (
        df["season_temp_1"].astype(str) + "-" + df["season_temp_2"].astype(str)
    )

    return df


def merge_elo_place_nr(df: pd.DataFrame, elo_df: pd.DataFrame, name: str):
    merged_df = pd.merge(
        df,
        elo_df,
        how="left",
        left_on=[f"{name}_team", "season_prev"],
        right_on=["Team", "season"],
    )
    merged_df = merged_df.rename(
        columns={"table_id": f"place_elo_{name}", "season_x": "season"}
    )
    merged_df = merged_df.drop(columns=["Team", "season_y"])

    return merged_df


def download_elo_data():
    """download 5 competition ELO ratings data, season 2019-2023"""
    df = scraping_elo.create_matches_data_table()
    df = _split_result(df)
    df = _split_season(df)

    unique_season_prev = df["season_prev"].unique()
    # seasons_list = ["2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022"]
    dff = scraping_elo.get_full_elo_ratings(seasons=unique_season_prev)
    elo = dff[["table_id", "Team", "season"]]

    # dft = pd.read_excel("./data/downloaded_data/matches_test.xlsx")
    # elo = pd.read_excel("./data/downloaded_data/elo_test.xlsx")

    merged_df = merge_elo_place_nr(df, elo_df=elo, name="home")
    merged_df = merge_elo_place_nr(merged_df, elo_df=elo, name="away")
    return merged_df

    # df.to_excel("./data/downloaded_data/matches1.xlsx")


# if "__main__" == __name__:
#    df = download_elo_data()
#
#    df.to_excel("./data/downloaded_data/.matches.xlsx")
