import pandas as pd
import re

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

import pickle
import time
from time import sleep


import wsc_config


class ParsingData:
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument("--disable-notifications")

        chrome_service = ChromeService(executable_path=wsc_config.CHROME_DRIVER_V117)
        self.driver = webdriver.Chrome(service=chrome_service, options=self.options)
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        # self.headers = {
        #    "Accept": "*/*",
        #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        # }

    def _pop_up_closer(self):
        try:
            self.driver.find_element(By.XPATH, wsc_config.AGREE_COOKIES_BUTTON).click()
            time.sleep(20)
        except NoSuchElementException:
            print("Cookies pop up not found")
            pass
        try:
            self.driver.execute_script(wsc_config.JS_POP_UP_CLOSE)
        except JavascriptException:
            print("Pop up not found")
            pass
        time.sleep(20)

    def get_cookies(self, url: str) -> str("html file"):
        """Get cookies from url"""
        self.driver.get(url)
        name = url.partition(".")[2].partition(".")[0]
        # time.sleep(30)
        pickle.dump(self.driver.get_cookies(), open(f"session_{name}", "wb"))
        # time.sleep(20)
        self.driver.quit()
        print("Cookies save")

    def _collect_leagues_hrefs(self) -> pd.DataFrame:
        """Collected all leagues hrefs

        Returns:
            pd.DataFrame: returned hrefs DataFrame by alphabetical list
        """
        comp = self.driver.find_element(By.ID, "domestic-regions").find_elements(
            By.CLASS_NAME, "t"
        )
        hrefs_dict = {"country": [], "competition": [], "hrefs": []}

        for i in comp:
            href = i.get_attribute("href")
            title = i.get_attribute("text")
            country = href.partition("-")[0].split("/")[len(href.split("/")) - 1]

            hrefs_dict["country"].append(country)
            hrefs_dict["competition"].append(title)
            hrefs_dict["hrefs"].append(href)

        hrefs_df = pd.DataFrame(hrefs_dict)
        return hrefs_df

    def _hrefs_collector(self) -> pd.DataFrame:
        """Collected all hrefs

        Returns:
            pd.DataFrame: full hrefs dataframe
        """
        self.driver.find_element(By.XPATH, wsc_config.ALL_LEAGUES_BUTTON).click()
        regions = self.driver.find_element(By.ID, "domestic-index")
        body_html = regions.get_attribute("innerHTML")
        soup = BeautifulSoup(body_html, "lxml")
        all_tags = soup.find_all("a")

        full_hrefs_df = []

        for i in range(2, len(all_tags) + 1):
            btn = wsc_config.ALPHABET_BUTTON.format(n=i)
            self.driver.find_element(By.XPATH, btn).click()
            hrefs_df = self._collect_leagues_hrefs()
            full_hrefs_df.append(hrefs_df)

        df = pd.concat(full_hrefs_df)

        return df

    def _season_hrefs_collector(self, url):
        self.driver.get(url)
        time.sleep(10)
        hrefs_season_list = self.driver.find_element(By.ID, "seasons").find_elements(
            By.TAG_NAME, "option"
        )

        hrefs_dict = {"href_element": [], "season": []}
        for e in hrefs_season_list:
            href_element = "https://www.whoscored.com/" + e.get_attribute("value")
            season = e.get_attribute("text")
            hrefs_dict["href_element"].append(href_element)
            hrefs_dict["season"].append(season)
            print(season)

        hrefs_df = pd.DataFrame(hrefs_dict)
        return hrefs_df

    def _season_collector(
        self, hrefs_data: pd.DataFrame = pd.read_excel(".\wsc_scraping\hrefs.xlsx")
    ):
        full_seasons_df = []
        for index, row in hrefs_data.iterrows():
            country = row["country"]
            comp = row["competition"]
            print(country, comp)
            iurl = row["hrefs"]
            season_hrefs_df = self._season_hrefs_collector(url=iurl)
            season_hrefs_df["country"] = country
            season_hrefs_df["competition"] = comp
            season_hrefs_df["original_url"] = iurl
            full_seasons_df.append(season_hrefs_df)

        df = pd.concat(full_seasons_df)
        return df

    def _stages_hrefs_collector(self):
        time.sleep(10)
        try:
            hrefs_stage_list = self.driver.find_element(By.ID, "stages").find_elements(
                By.TAG_NAME, "option"
            )
        except NoSuchElementException:
            print(f"Error: STAGES Not Found")
            return None

        hrefs_dict = {"competition_exp": [], "href": []}

        for i in hrefs_stage_list:
            title = i.get_attribute("text")
            href = "https://www.whoscored.com/" + i.get_attribute("value")
            hrefs_dict["competition_exp"].append(title)
            hrefs_dict["href"].append(href)

        df = pd.DataFrame(hrefs_dict)
        return df

    def _collect_headers_hrefs(self):
        fixtures_href = self.driver.find_element(By.ID, "sub-navigation").find_elements(
            By.TAG_NAME, "a"
        )
        detail_hrefs = {
            "Summary": [],
            "Fixtures": [],
            "Team Statistics": [],
            "Player Statistics": [],
            "Referee Statistics": [],
        }
        for i in fixtures_href:
            header = i.get_attribute("text")
            href = i.get_attribute("href")
            detail_hrefs[header].append(href)

        for key in detail_hrefs:
            if not detail_hrefs[key]:
                detail_hrefs[key] = None

        df = pd.DataFrame(detail_hrefs)
        return df

    # Čia reikės daryti pagal iterrows() ir perduoti url pagal season, country, season, league o po to papildomai prisidės league
    def _stats_hrefs_collector(self, url: str, comp: str):
        self.driver.get(url)

        df_comp_bonus = self._stages_hrefs_collector()

        if df_comp_bonus is not None:
            # hrefs = df_comp_bonus["href"].unique()
            df_list = []
            for index, row in df_comp_bonus.iterrows():
                _url = row["href"]
                competition_exp = row["competition_exp"]
                self.driver.get(_url)
                headers_href_df = self._collect_headers_hrefs()
                headers_href_df["competition_exp"] = competition_exp
                df_list.append(headers_href_df)
            full_headers_df = pd.concat(df_list)
        else:
            full_headers_df = self._collect_headers_hrefs()
            full_headers_df["competition_exp"] = comp

        return full_headers_df

    def _headers_hrefs_main_collector(self, df: pd.DataFrame):
        df_list = []
        for index, row in df.iterrows():
            url = row["href_element"]
            season = row["season"]
            country = row["country"]
            competition = row["competition"]
            original_href = row["original_url"]
            stats_hrefs = self._stats_hrefs_collector(url=url, comp=competition)
            stats_hrefs["url_detail"] = url
            stats_hrefs["season"] = season
            stats_hrefs["country"] = country
            stats_hrefs["competition_main"] = competition
            stats_hrefs["original_href"] = original_href
            print(competition, season)
            df_list.append(stats_hrefs)

        df = pd.concat(df_list)

        return df

    def _collect_matches_hrefs(self):
        # divtable_body = self.driver.find_element(By.CLASS_NAME, "divtable-body")

        # wait = WebDriverWait(self.driver, 10)
        # result_links = wait.until(
        #    EC.presence_of_all_elements_located((By.CLASS_NAME, "result-1.rc"))
        # )
        time.sleep(10)
        result_links = self.driver.find_elements(By.CLASS_NAME, "result-1.rc")

        hrefs_list = {"href_matches": []}
        for link in result_links:
            href = link.get_attribute("href")
            hrefs_list["href_matches"].append(href)

        df = pd.DataFrame(hrefs_list)

        # self.driver.switch_to.default_content()

        return df

    def _menu_date_navigation(self, collector):
        date_buttons = [wsc_config.FIRST_DATE_BUTTON, wsc_config.SECOND_DATE_BUTTON]
        date_rows = [1, 2, 3]
        date_columns = [1, 2, 3, 4]

        collected_data = []
        for btn in date_buttons:
            # print(f"menu button clicked {btn}")
            year_table = self.driver.find_element(By.CLASS_NAME, "part").find_elements(
                By.TAG_NAME, "td"
            )
            print(f"elements in year table: {len(year_table)}")
            if len(year_table) <= 1:
                pass
            else:
                try:
                    self.driver.find_element(By.XPATH, btn).click()
                except:
                    print("Error prie click year")

            print("Click succes")
            for row in date_rows:
                for col in date_columns:
                    button = self.driver.find_element(
                        By.XPATH,
                        wsc_config.MONTHS_BUTTON.format(date_row_x=row, date_col_x=col),
                    )
                    button_class = button.get_attribute("class")
                    if "selectable" in button_class:
                        button.click()
                        collected_data.append(collector())
                        # print(f"click row: {row}, col: {col}")
        dff = pd.concat(collected_data)
        dff = dff.drop_duplicates()
        return dff

    def _collect_matches_href_main(self, df: pd.DataFrame):
        df_list = []
        for index, row in df.iterrows():
            url = row["Fixtures"]
            competition_exp = row["competition_exp"]
            season = row["season"]
            country = row["country"]
            competition_main = row["competition_main"]
            print(url)
            self.driver.get(url)
            self._pop_up_closer()
            self.driver.find_element(
                By.XPATH, wsc_config.DATE_MENU_NAV_BUTTON
            ).click()  # expand date menu
            print("Expand menu")
            time.sleep(5)
            df = self._menu_date_navigation(collector=self._collect_matches_hrefs)
            df["competition_exp"] = competition_exp
            df["season"] = season
            s = str(season).replace("/", "_")
            df["country"] = country
            df["competition_main"] = competition_main
            df.to_excel(f"./wsc_scraping/data/matche_href_{s}_{competition_exp}.xlsx")
            df_list.append(df)
        dff = pd.concat(df_list)
        dff.to_excel("./wsc_scraping/matches_hrefs.xlsx")

    def _collect_match_headers_hrefs(
        self, url
    ):  # kartojasi, reikės perkelti kaip vieną
        self.driver.get(url)

        fixtures_href = self.driver.find_element(By.ID, "sub-navigation").find_elements(
            By.TAG_NAME, "a"
        )
        detail_hrefs = {}
        for i in fixtures_href:
            header = i.get_attribute("text")
            href = i.get_attribute("href")
            detail_hrefs[header] = href

        for key in detail_hrefs:
            if not detail_hrefs[key]:
                detail_hrefs[key] = None

        df = pd.DataFrame(detail_hrefs, index=[0])
        return df

    def _stats_group(self):
        stats_preematch_container = self.driver.find_elements(
            By.CLASS_NAME, "stat-group"
        )

        df_dict = {}
        counter = 0
        for i in stats_preematch_container:
            if counter == 0:
                counter += 1
                continue
            stat_group = i.find_elements(By.CLASS_NAME, "stat")
            for s in stat_group:
                element_text = s.text
                text_without_parentheses = (
                    re.sub(r"\([^)]*\)", "", element_text).strip().replace("%", "")
                )

                detail = re.match(
                    r"(\d+\.\d+)\s+(.*?)\s+(\d+\.\d+)", text_without_parentheses
                )
                if detail:
                    home_header = "home_" + detail.group(2)
                    home_num = float(detail.group(1))
                    away_header = "away_" + detail.group(2)
                    away_num = float(detail.group(3))

                    df_dict[home_header] = home_num
                    df_dict[away_header] = away_num
                else:
                    print("Text not found")

                break

        dff = pd.DataFrame(df_dict)
        print(dff)

    def _scrap_preview(self, url):
        self.driver.get(url)
        time.sleep(10)
        match_header = self.driver.find_element(By.ID, "match-header")

        home_team = match_header.find_element(
            By.CSS_SELECTOR, '.home[class*="home"] .team-link'
        ).get_attribute("text")

        away_team = match_header.find_element(
            By.CSS_SELECTOR, '.away[class*="away"] .team-link'
        ).get_attribute("text")

        probalbly_lineups = self.driver.find_element(By.ID, "preview-lineups")
        home_team_html = probalbly_lineups.find_element(By.CLASS_NAME, "home")
        home_formation = home_team_html.find_element(
            By.CLASS_NAME, "formation-label"
        ).text

        away_team_html = probalbly_lineups.find_element(By.CLASS_NAME, "away")
        away_formation = away_team_html.find_element(
            By.CLASS_NAME, "formation-label"
        ).text
        self._stats_group()

        print(home_team, " ", home_formation, " ", away_team, " ", away_formation)

    def _scrap_stats(self):
        pass

    def _create_matches_stats_df(self):
        # for index, row in df.iterrows():
        url = "https://www.whoscored.com/Matches/1649514/Preview/England-League-Two-2022-2023-Hartlepool-Harrogate-Town"
        # url = row["href_matches"]
        # competition_exp = row['competition_exp']
        # season = row['season']
        # country = row['country']
        # competition_main = row['competition_main']
        self.driver.get(url)
        headers_hrefs = self._collect_match_headers_hrefs(url=url)
        url_preview = headers_hrefs["Preview"][0]
        # url_stats = headers_hrefs["Match Centre"]
        self._scrap_preview(url=url_preview)

        print(url_preview)

    def entry_wsc(self):
        # url = wsc_config.WEB
        # self.driver.get(url)
        # for cookies in pickle.load(open(wsc_config.WSC_COOKIES, "rb")):
        #    self.driver.add_cookie(cookies)
        # self.driver.refresh()
        #
        # self.driver.find_element(By.XPATH, wsc_config.AGREE_COOKIES_BUTTON).click()
        # hrefs_df = self._hrefs_collector()
        # df = self._season_collector()

        # df = pd.read_excel("./wsc_scraping/stats_hrefs.xlsx")
        # df = df.loc[df['competition']=='League One']
        # self._collect_matches_href_main(df=df)
        df = self._create_matches_stats_df()

        print(df)
        # print("pop up disabled")
        time.sleep(10)
        self.driver.quit()


if "__main__" == __name__:
    p = ParsingData()
    p.entry_wsc()
