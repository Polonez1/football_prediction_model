import pandas as pd

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

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

    def get_cookies(self, url: str) -> str("html file"):
        """Get cookies from url"""
        self.driver.get(url)
        name = url.partition(".")[2].partition(".")[0]
        # time.sleep(30)
        pickle.dump(self.driver.get_cookies(), open(f"session_{name}", "wb"))
        # time.sleep(20)
        self.driver.quit()
        print("Cookies save")

    def _collect_leagues_hrefs(self):
        comp = self.driver.find_element(By.ID, "domestic-regions").find_elements(
            By.CLASS_NAME, "t"
        )
        for i in comp:
            href = i.get_attribute("href")
            print(href)

    def _leagues_loop(self):
        self.driver.find_element(By.XPATH, wsc_config.ALL_LEAGUES_BUTTON).click()
        regions = self.driver.find_element(By.ID, "domestic-index")
        body_html = regions.get_attribute("innerHTML")
        soup = BeautifulSoup(body_html, "lxml")
        all_tags = soup.find_all("a")
        for i in range(2, len(all_tags) + 1):
            btn = wsc_config.ALPHABET_BUTTON.format(n=i)
            self.driver.find_element(By.XPATH, btn).click()
            self._collect_leagues_hrefs()

            break

    def entry_wsc(self):
        url = wsc_config.WEB
        self.driver.get(url)
        for cookies in pickle.load(open(wsc_config.WSC_COOKIES, "rb")):
            self.driver.add_cookie(cookies)
        self.driver.refresh()

        self.driver.find_element(By.XPATH, wsc_config.AGREE_COOKIES_BUTTON).click()
        self._leagues_loop()

        print("pop up disabled")
        time.sleep(180)
        self.driver.quit()


if "__main__" == __name__:
    p = ParsingData()
    p.entry_wsc()
