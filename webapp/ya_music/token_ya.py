import json
from time import sleep

# import os
from flask_login import current_user
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By

from webapp import db
from webapp.user.models import User

# CACHES_FOLDER = 'webapp/ya_music/yandex_caches/'
# if not os.path.exists(CACHES_FOLDER):
#     os.makedirs(CACHES_FOLDER)


def is_active(driver):
    try:
        driver.execute(Command.GET_ALL_COOKIES)
        return True
    except Exception:
        return False


# def token_cache_path():
#     return CACHES_FOLDER + str(current_user.id) + '.txt'

def sel_driver():
    # make chrome log requests
    capabilities = DesiredCapabilities.CHROME
    capabilities["loggingPrefs"] = {"performance": "ALL"}
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Remote(desired_capabilities=capabilities,
                              command_executor="http://selenium:4444/wd/hub")
    driver.get(
        "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d"
    )

    driver.find_element(By.XPATH, "//span[text()='QR-код']").click()
    sleep(5)
    qr_code = driver.find_element(By.CLASS_NAME, "MagicField-qr")
    # print(qr_code)
    qr_url = qr_code.value_of_css_property('background-image')
    # print(qr_url)
    qr_url = qr_url.split('"')[1]
    print(qr_url)
    print(type(qr_url))
    # driver.get(qr_url)
    # КНОПКА ПОДТВЕРДИТЬ ВХОД
    driver.find_element(By.XPATH, "//button[type='submit']").click()


    return qr_url, driver


def get_token(driver):
    # user_login = "makar.tim@example.com"

    # driver.find_element(By.ID, "passp-field-login").send_keys(user_login)
    # driver.find_element(By.ID, "passp-field-login").send_keys(user_login)

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

    User.query.filter(User.id == current_user.id).update(dict(yandex_token=token))
    db.session.commit()

    try:
        driver.close()
    except Exception:
        pass

    # try:
    #     driver.close()
    # except:
    #     pass
    # cache_path = token_cache_path()
    # try:
    #     f = open(cache_path, "w")
    #     f.write(token)
    #     f.close()
    # except IOError:
    #     print('Couldn\'t write token to cache at: %s', cache_path)


# def get_cach_token(token_path):
#     token_info = ''
#     try:
#         f = open(token_path)
#         token_info = f.read()
#         f.close()

#     except IOError as error:
#         print("Couldn't read cache at: %s", {token_path})
#     return token_info
