import json
from time import sleep

# import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By

from webapp.db import db
from webapp.user.models import User


def is_active(driver):
    try:
        driver.execute(Command.GET_ALL_COOKIES)
        return True
    except Exception:
        return False


# def token_cache_path():
#     return CACHES_FOLDER + str(current_user.id) + '.txt'

def yandex_ouath(email, password, user_id):
    # make chrome log requests
    capabilities = DesiredCapabilities.CHROME
    capabilities["loggingPrefs"] = {"performance": "ALL"}
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://selenium:4444/wd/hub")
    driver.get(
        "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d"
    )
    sleep(5)
    driver.find_element(By.ID, "passp-field-login").send_keys(email)
    driver.find_element(By.ID, "passp:sign-in").click()
    sleep(5)
    driver.find_element(By.ID, "passp-field-passwd").send_keys(password)
    driver.find_element(By.ID, "passp:sign-in").click()
    # try:
    #     sleep(1)
    #     driver.find_element(By.CLASS_NAME, "Authorize-button").click()
    # except Exception:
    #     print('No accept Button')

    token = None

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

    print(token)

    User.query.filter(User.id == user_id).update(dict(yandex_token=token))
    db.session.commit()

    try:
        driver.close()
    except Exception:
        pass


# def get_token(driver):
#     token = None

#     while token is None and is_active(driver):
#         sleep(1)
#         try:
#             logs_raw = driver.get_log("performance")
#         except Exception:
#             pass

#         for lr in logs_raw:
#             log = json.loads(lr["message"])["message"]
#             url_fragment = log.get("params", {}).get("frame", {}).get("urlFragment")

#             if url_fragment:
#                 token = url_fragment.split("&")[0].split("=")[1]

#     print(token)
#     return token
