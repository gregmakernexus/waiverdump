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
            if not ('userid' in config and 'password' in config):
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
    driver = webdriver.Chrome()
    driver.get("https://app.resmarksystems.com/login/")
    try:
        button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "loginButton")))
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
        # If the login was not successful, there will be a 30-second timeout.
        menu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "waiversign")))
        driver.execute_script('arguments[0].scrollIntoView(false);', menu)
        if menu is None:
            print("Login timeout.  Deleting configuration.  Re-run program")
            os.remove(config_name)
            exit(-1)
        time.sleep(5)
        # when chrome is not logged in the side menu is hidden and needs to be popped up
        make_side_menu_appear(driver)
        menu2 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "signedDocumentsNav")))
        driver.execute_script('arguments[0].scrollIntoView(false);', menu2)
        # menu = wait_till_found(driver, By.ID, "signedDocumentsNav")
        time.sleep(1)
        menu2.click()
        print(" ")
    except Exception:
        traceback.print_exc()
        exit(-2)
    # --------------------------------------------------------------
    # Click on the "export contacts" link
    # --------------------------------------------------------------
    try:
        # Now we need to make sure the menu is hidden
        make_side_menu_disappear(driver)
        btn2 = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Export Contacts")))
        driver.execute_script('arguments[0].scrollIntoView(false);', btn2)
        btn2.click()
    except Exception:
        time.sleep(2)
        traceback.print_exc()
        exit(-2)
    # --------------------------------------------------------------
    # Click on the "signed documents" menu
    # --------------------------------------------------------------
    try:
        btn_xpath = "//div[@id='exportContact']//div[@class='actions']//div[@role='button']"
        WebDriverWait(driver, 20).until(EC.visibility_of(driver.find_element(By.XPATH, btn_xpath)))
        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
        driver.execute_script('arguments[0].scrollIntoView(false);', btn)
        btn.click()
    except Exception:
        traceback.print_exc()
        exit(-2)

    try:
        filename = wait_till_file(waiver_list)
        if filename is not None:
            print("file successfully downloaded:", filename)
    except Exception:
        traceback.print_exc()
        exit(-3)


def make_side_menu_appear(driver):
    for i in range(3):
        try:
            menu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "waiversign")))
            menu.click()
            side_menu = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "signedDocumentsNav")))
            if side_menu.is_displayed():
                print("side menu is visible")
                break
            time.sleep(5)
            print("LOOP in make_side_menu_appear")

        except Exception as err:
            print("*******\n", err)
            print("timeout")
    return


def make_side_menu_disappear(driver):
    for i in range(3):
        try:
            WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.ID, "signedDocumentsNav")))
        except Exception:
            menu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "waiversign")))
            driver.execute_script('arguments[0].scrollIntoView(false);', menu)
            menu.click()
            time.sleep(1)
    return


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
    config = {'userid': userid, 'password': password}
    with open(config_name, 'w') as outfile:
        json.dump(config, outfile)
    return config


if __name__ == "__main__":
    main()
