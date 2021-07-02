import requests
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from src.utils import parse_string
import logging

logger = logging.Logger(__name__)


def search_google_trans(driver, source_language="en", target_language="vi", text_to_translate=None):
    """
        Translate by search
        Translate the parameter text_to_translate from the source_language to the
        target_language, by getting this info from the Google Translate site.
        Parameters are all strings.
        Return is None.
    """
    # exit the function if no text is submitted
    if not text_to_translate:
        print("No text submitted.\nPlease insert a text.\n")
        return None

    if text_to_translate.startswith("http"):
        text_to_translate = requests.get(text_to_translate).text

    elif text_to_translate.endswith(".txt"):
        with open(text_to_translate, encoding="UTF-8") as file:
            text_to_translate = file.read()

    # variables to be used in the url:
    # source language
    sl = source_language
    # target language
    tl = target_language
    # operation
    operation = "translate"

    text_to_translate = parse_string(text_to_translate)
    # f-string with variables:
    link = f"https://translate.google.com/?sl={sl}&tl={tl}&text={text_to_translate}&op={operation}"
    # open the link in the browser
    driver.get(link)

    # wait for 10 seconds to page to load
    time.sleep(10)

    translation_text = driver.find_element_by_css_selector('#yDmH0d > c-wiz > div > div.WFnNle > c-wiz > div.OlSOob > c-wiz > div.ccvoYb > div.AxqVh > div.OPPzxe > c-wiz.P6w8m.BDJ8fb > div.dePhmb > div > div.J0lOec > span.VIiyi > span > span')
    driver.quit()
    return translation_text


def translate(driver, wait, source_language="en", target_language="vi", text=None):
    try:
        link = f"https://translate.google.com/?hl=vi#view=home&op=translate&sl={source_language}&tl={target_language}"
        if driver.current_url != link:
            driver.get(link)
            wait = WebDriverWait(driver, 20)

        input_area = driver.find_element_by_xpath(
            '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/span/span/div/textarea')
        input_area.clear()
        time.sleep(0.8)
        input_area.send_keys(text)
        translated_text = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ow314"]/div[1]/span[1]/span'))).text
        return translated_text
    except Exception as e:
        logger.debug(f"Translate error {e}: \nText: {text}")
        return ''
