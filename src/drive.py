from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def create_chrome_driver(chrome_path, proxy=None):
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    return driver
