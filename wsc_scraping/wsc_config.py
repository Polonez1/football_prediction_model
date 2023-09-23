CHROME_DRIVER_V117 = r"./wsc_scraping/chromedriver.exe"


WEB = "https://www.whoscored.com/"
WSC_COOKIES = ".\wsc_scraping\session_whoscored"


# Buttons

AGREE_COOKIES_BUTTON = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'
JS_POP_UP_CLOSE = (
    "document.querySelector('.webpush-swal2-container').style.display = 'none';"
)
FIRST_DATE_BUTTON = (
    '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[1]/div/table/tbody/tr[1]/td'
)
SECOND_DATE_BUTTON = (
    '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[1]/div/table/tbody/tr[2]/td'
)

MONTHS_BUTTON = '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr[{date_row_x}]/td[{date_col_x}]'


ALL_LEAGUES_BUTTON = '//*[@id="tournament-groups"]/li[3]'

ALPHABET_BUTTON = '//*[@id="domestic-index"]/dd[{n}]'


DATE_MENU_NAV_BUTTON = '//*[@id="date-config-toggle-button"]'
