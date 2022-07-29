import json
from time import sleep

# import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
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

def sel_driver():
    # make chrome log requests
    capabilities = DesiredCapabilities.CHROME
    capabilities["loggingPrefs"] = {"performance": "ALL"}
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://selenium:4444/wd/hub")
    driver.get(
        "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d"
    )
    sleep(2)
    driver.find_element(By.XPATH, "//span[text()='QR-код']").click()

    sleep(2)
    qr_code = driver.find_element(By.CLASS_NAME, "MagicField-qr")
    qr_url = qr_code.value_of_css_property('background-image')
    qr_url = qr_url.split('"')[1]
    command_executor_url = driver.command_executor._url
    session_id = driver.session_id
    print(command_executor_url)
    print(session_id)

    return qr_url, command_executor_url, session_id


def get_token(url, session_id, user_id):
    # user_login = "makar.tim@example.com"

    # driver.find_element(By.ID, "passp-field-login").send_keys(user_login)
    # driver.find_element(By.ID, "passp-field-login").send_keys(user_login)

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    capabilities = DesiredCapabilities.CHROME
    capabilities["loggingPrefs"] = {"performance": "ALL"}
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    new_driver = webdriver.Remote(command_executor=url, desired_capabilities=capabilities)
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    driver = new_driver
    print(driver.current_url)
    print(is_active(driver))
    print(driver.session_id)

    while is_active(driver):
        try:
            sleep(1)
            driver.find_element(By.CLASS_NAME, "MagicField-qr")
            print('Qr-code still on the page')
        except Exception:
            try:
                sleep(1)
                driver.find_element(By.CLASS_NAME, "Authorize-button").click()
            except Exception:
                print('No accept Button')

            token = None
            print("I'm here!!!!!!!!!")

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
            sleep(20)
            # try:
            #     driver.close()
            # except Exception:
            #     pass
