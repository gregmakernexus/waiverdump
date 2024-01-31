import glob
import os
import time
import traceback
import json
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path


def main():
    home = Path.home()
    download = os.path.join(home, "Downloads")
    waiver_list = os.path.join(download, "WaiverSign*.*")
    # ------------------------------------------------------
    # Get the config file
    # ------------------------------------------------------
    config_name = os.path.join(home, ".waiversign.json")
    if os.path.isfile(config_name):
        with open(config_name) as json_file:
            config = json.load(json_file)
            if not ('userid' in config or 'password' in config):
                print("invalid configuration.  Re-initializing.")
                config = init_config(config_name)
    else:
        config = init_config(config_name)
    # ------------------------------------------------------
    # Delete all the downloaded files
    # ------------------------------------------------------
    _filelist = glob.glob(waiver_list, recursive=False)
    for file in _filelist:
        try:
            os.remove(file)
        except OSError:
            print("Error while deleting file")
    # -----------------------------------------------------
    # Open Chrome and login to waiversign
    # ------------------------------------------------------
    driver = webdriver.chromium.webdriver.Chromiumdriver()
    driver.get("https://app.resmarksystems.com/login/")
    try:
        button = wait_till_found(driver, By.ID, "loginButton")
        username = driver.find_element(By.ID, "username")

        username.send_keys(config['userid'])
        password = driver.find_element(By.ID, "password")
        password.send_keys(config['password'])
        button.click()

    except Exception:
        print("Login page has changed.  Field id missing")
        traceback.print_exc()
        exit(-1)
    # --------------------------------------------------------------
    # Click on the "signed documents" menu
    # --------------------------------------------------------------
    try:
        # make sure the buttons
        menu = wait_till_found(driver, By.ID, "waiversign")
        menu.click()

        menu = wait_till_found(driver, By.ID, "signedDocumentsNav")
        menu.click()
        print(" ")
    except Exception:
        traceback.print_exc()
        exit(-2)
    # --------------------------------------------------------------
    # Click on the "export contacts" link
    # --------------------------------------------------------------
    try:
        menu = wait_till_found(driver, By.ID, "signedDocumentsNav")
        if menu is not None:
            menu = wait_till_found(driver, By.ID, "waiversign")
            menu.click()
            WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, "signedDocumentsNav")))

        wait_till_found(driver, By.PARTIAL_LINK_TEXT, "Export Contacts")
        btn2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Export Contacts")))
        driver.execute_script('arguments[0].scrollIntoView(false);', btn2)
        btn2.click()
    except Exception:
        traceback.print_exc()
        exit(-2)
    # --------------------------------------------------------------
    # Click on the "signed documents" menu
    # --------------------------------------------------------------
    try:
        btn_xpath = "//div[@id='exportContact']//div[@class='actions']//div[@role='button']"
        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
        driver.execute_script('arguments[0].scrollIntoView(false);', btn)
        btn.click()
    except Exception:
        traceback.print_exc()
        exit(-2)

    try:
        filename = wait_till_file(waiver_list)
        if filename is not None:
            config['file'] = filename
            print(config)
            with open(config_name, 'w') as outfile:
                json.dump(config, outfile)
            print("file successfully downloaded:", filename)

    except Exception:
        traceback.print_exc()
        exit(-3)


def wait_till_found(driver, method, _id):
    for i in range(10):
        try:
            element = driver.find_element(method, _id)
            return element

        except Exception:
            time.sleep(1)
    return None


def wait_till_file(f):
    for i in range(30):
        files = glob.glob(f)
        for j in range(len(files)):
            if "crdownload" not in files[j]:
                return files[j]
        time.sleep(1)
    return None


def init_config(config_name):
    print("waiversign login information")
    userid = input("Please enter user id:\n")
    # regex for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, userid):
        print("Userid must be a Valid Email")
        traceback.print_exc()
    password = input("Please enter password:\n")
    config = {'userid': userid, 'password': password, 'file': ""}
    with open(config_name, 'w') as outfile:
        json.dump(config, outfile)
    return config


if __name__ == "__main__":
    main()
