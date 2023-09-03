import pandas as pd

# import numpy as np
import requests
from bs4 import BeautifulSoup

# from selenium import webdriver
# from selenium_stealth import stealth
# from selenium.webdriver.common.by import By

# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

import elo_config

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


class ParsingData:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(
            options=self.options,
            executable_path=r".\\scraping\\chromedriver.exe",
            service=Service(ChromeDriverManager().install()),
        )
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import elo_config

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


class ParsingData:
    def __init__(self):
        #        self.options = webdriver.ChromeOptions()
        #        self.options.add_argument("start-maximized")
        #        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #        self.options.add_experimental_option("useAutomationExtension", False)
        #        self.options.add_argument("--disable-notifications")
        #        self.driver = webdriver.Chrome(
        #            options=self.options,
        #            executable_path=r".\\scraping\\chromedriver.exe",
        #            service=Service(ChromeDriverManager().install()),
        #        )
        #        stealth(
        #            self.driver,
        #            languages=["en-US", "en"],
        #            vendor="Google Inc.",
        #            platform="Win32",
        #            webgl_vendor="Intel Inc.",
        #            renderer="Intel Iris OpenGL Engine",
        #            fix_hairline=True,
        #        )
        #
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }


def _replace_empty_to_none(data_list):
    new_list = []
    for item in data_list:
        new_item = {
            key: (None if value == "" else value) for key, value in item.items()
        }
        new_list.append(new_item)
    return new_list


def conn_to_elo(country, season):
    elo = ParsingData()
    web = elo_config.ELO_WEB_BY_COUNTRY.format(country=country, season=season)
    req = requests.get(url=web, headers=elo.headers)
    return req


def create_soup(req):
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    return soup


def _rename_elo_matches_columns(df: pd.DataFrame):
    df = df.drop("Unnamed: 2", axis=1)
    df = df.drop("Unnamed: 15", axis=1)
    df = df.rename(
        columns={
            "Home": "home_team",
            "Unnamed: 4": "home_elo",
            "→": "home_elo_change",
            "Unnamed: 6": "home_elo_final",
            "Probabilities: H": "home_prb",
            "D": "draw_prb",
            "A": "away_prb",
            "Away": "away_team",
            "Unnamed: 12": "away_elo",
            "→.1": "away_elo_change",
            "Unnamed: 14": "away_elo_final",
        },
        inplace=False,
    )

    return df


def _parsing_body(table_data, country):
    elo_data_table = []
    count = 0
    for item in table_data:
        elo_data = item.find_all("td")
        if elo_data != []:
            table_id = elo_data[0].text.strip()
            Team = elo_data[1].text.strip()
            F1 = elo_data[2].text.strip()
            F2 = elo_data[3].text.strip()
            F3 = elo_data[4].text.strip()
            F4 = elo_data[5].text.strip()
            F5 = elo_data[6].text.strip()
            F6 = elo_data[7].text.strip()
            rating = elo_data[8].text.strip()
            record = elo_data[9].text.strip()
            all_time = elo_data[10].text.strip()
            diff = elo_data[11].text.strip()
            Y1 = elo_data[12].text.strip()
            season_to_date = elo_data[13].text.strip()
            league = elo_data[14].text.strip()
            cup = elo_data[15].text.strip()
            europe = elo_data[16].text.strip()
            uefa = elo_data[17].text.strip()
            di = {
                "table_id": table_id,
                "country": country,
                "Team": Team,
                "F1": F1,
                "F2": F2,
                "F3": F3,
                "F4": F4,
                "F5": F5,
                "F6": F6,
                "rating": rating,
                "record": record,
                "all_time": all_time,
                "diff": diff,
                "Y1": Y1,
                "season_to_date": season_to_date,
                "league": league,
                "cup": cup,
                "europe": europe,
                "uefa": uefa,
            }
            elo_data_table.append(di)
            count = count + 1
        else:
            continue

    elo_data_table_with_none = _replace_empty_to_none(elo_data_table)
    df = pd.DataFrame(elo_data_table_with_none)

    return df


def parsing_elo_matches(country, season):
    url = elo_config.ELO_WEB_BY_COUNTRY.format(country=country, season=season)
    tables = pd.read_html(url)
    return tables[4]


def parsing_elo_web(country, season):
    req = conn_to_elo(country=country, season=season)
    soup = create_soup(req=req)

    country = soup.find(id="ranking").find("h3").find("b").text.strip()
    table_data = soup.find(id="Ranking").find(id="body").find("table").find_all("tr")

    df = _parsing_body(table_data=table_data, country=country)

    return df


def create_last_elo_ranking_table(season="2023-2024"):
    competition_list = elo_config.COUNTRY_LIST

    full_df = []
    for comp in competition_list:
        df = parsing_elo_web(country=comp, season=season)
        full_df.append(df)

    dff = pd.concat(full_df)
    return dff


def create_matches_data_table():
    full_df = []
    for season in elo_config.SEASON_LIST:
        print(season)
        for comp in elo_config.COUNTRY_LIST:
            _df = parsing_elo_matches(country=comp, season=season)
            df = _rename_elo_matches_columns(_df)
            df["Date"].fillna(method="ffill", inplace=True)
            full_df.append(df)
            print(comp)

    dff = pd.concat(full_df)
    dff.to_excel("./scraping/matches.xlsx")
    return dff


def get_elo_by_team(team: str, season="2023-2024"):
    df = create_last_elo_ranking_table(season=season)
    df_team = df.loc[df["Team"] == team]
    df_team_elo = df_team[["Team", "rating"]]

    return df_team_elo


if "__main__" == __name__:
    df = create_matches_data_table()

    print(len(df))
