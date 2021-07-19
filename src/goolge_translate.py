import sys

import requests
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from src import PROXIES
from src.utils import parse_string
import logging

logger = logging.getLogger(__name__)


def check_search(driver):
    sl = 'en'
    # target language
    tl = 'vi'
    # operation
    operation = "translate"

    text_to_translate = 'how are you'
    link = f"https://translate.google.com/?sl={sl}&tl={tl}&text={text_to_translate}&op={operation}"
    # open the link in the browser
    driver.get(link)
    time.sleep(1)
    driver.quit()
    return False


def search_google_trans(driver: Chrome, wait: WebDriverWait, source_language="en", target_language="vi", text=None):
    """
        Translate by search
        Translate the parameter text_to_translate from the source_language to the
        target_language, by getting this info from the Google Translate site.
        Parameters are all strings.
        Return is None.
    """
    # exit the function if no text is submitted
    if not text:
        print("No text submitted.\nPlease insert a text.\n")
        return None

    # variables to be used in the url:
    # source language
    sl = source_language
    # target language
    tl = target_language
    # operation
    operation = "translate"

    text_to_translate = parse_string(text)
    # f-string with variables:

    link = f"https://translate.google.com/?sl={sl}&tl={tl}&text={text_to_translate}&op={operation}"
    # open the link in the browser
    driver.get(link)
    xpath = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]'

    try:
        # wait for t seconds to page to load
        translation_element = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        translation_text = translation_element.text
        return translation_text
    except Exception as e:
        try:
            # open the link in the browser
            driver.get(link)
            # wait for t seconds to page to load
            time.sleep(2)
            translation_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            translation_text = translation_element.text
            return translation_text
        except:
            print(f"Translate error {e}")
            return None


def translate(driver: Chrome, wait, source_language="en", target_language="vi", text=None):
    xpath = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]'
    try:
        link = f"https://translate.google.com/?hl=vi#view=home&op=translate&sl={source_language}&tl={target_language}"
        if driver.current_url != link:
            driver.get(link)
            wait = WebDriverWait(driver, 3)

        input_area = driver.find_element_by_xpath(
            '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/span/span/div/textarea')
        # input_area = driver.find_element_by_class_name('QFw9Te')

        input_area.clear()
        time.sleep(0.8)
        input_area.send_keys(text)
        time.sleep(0.8)

        translation_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        translated_text = translation_element.text
        return translated_text
    except Exception as e:
        print(f"Translate error {e}")
        return ''
