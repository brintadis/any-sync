"""
Yandex token processing
"""
import json
from time import sleep
from flask_login import current_user

# import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By

from webapp.db import db
from webapp.user.models import User


def is_active(driver):
    """
    Check if selenium driver is active
    """
    try:
        driver.execute(Command.GET_ALL_COOKIES)
        return True
    except Exception:
        return False


def close_webdriver(driver):
    """
    Close selenium webdriver
    """
    try:
        driver.close()
        driver.quit()
    except Exception:
        pass


# def token_cache_path():
#     return CACHES_FOLDER + str(current_user.id) + '.txt'

def yandex_ouath(email, password):
    """
    Yandex auth using selenium webdriver
    """
    # make chrome log requests
    capabilities = DesiredCapabilities.CHROME
    capabilities["loggingPrefs"] = {"performance": "ALL"}
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=800,600")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        desired_capabilities=capabilities,
        command_executor="http://selenium:4444/wd/hub",
        options=options,
        )
    driver.get(
        "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d"
    )

    sleep(2)
    print(f'Email: {email}, password: {password}')
    driver.find_element(By.ID, "passp-field-login").send_keys(email)
    driver.find_element(By.ID, "passp:sign-in").click()
    sleep(2)

    try:
        driver.find_element(By.ID, "passp-field-confirmation-code")
        close_webdriver(driver)
        return False, 'Неправильная электронная почта'
    except NoSuchElementException:
        pass

    driver.find_element(By.ID, "passp-field-passwd").send_keys(password)
    driver.find_element(By.ID, "passp:sign-in").click()

    try:
        sleep(1)
        driver.find_element(By.ID, "field:input-passwd:hint")
        close_webdriver(driver)
        return False, 'Неверный пароль'
    except NoSuchElementException:
        pass

    token = get_token(driver)

    if token is None:
        return False, 'Ошибка при авторизации, пожалуйста, попробуйте еще раз'

    return token, "Вы успешно авторизовались через Яндекс"


def get_token(driver):
    """
    Extracting token from logs, saving into db
    """

    token = None

    print(f"Token: {token}")

    while token is None and is_active(driver):
        sleep(1)
        try:
            logs_raw = driver.get_log("performance")
        except Exception:
            pass

        for lr in logs_raw:
            log = json.loads(lr["message"])["message"]
            url_fragment = log.get("params", {}).get("frame", {}).get("urlFragment")

            if url_fragment:
                token = url_fragment.split("&")[0].split("=")[1]

    print(f"Token: {token}")

    User.query.filter(User.id == current_user.id).update(dict(yandex_token=token))
    db.session.commit()

    close_webdriver(driver)

    return token
