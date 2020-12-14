from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
import platform

def getChromeDriverDir():
    CHROME_DRIVER = os.path.abspath(os.path.dirname(os.getcwd())) + os.sep + 'chromedriver' + os.sep
    if platform.system() == 'Windows':
        CHROME_DRIVER = os.getcwd() + os.sep + 'app\\api\data_getter\chromedriver.exe'
    if platform.system() == 'Linux':
        CHROME_DRIVER = os.getcwd() + os.sep + 'app/api/data_getter/chromedriver'
    if platform.system() == 'Darwin':
        CHROME_DRIVER = os.getcwd() + os.sep + 'app/api/data_getter/chromedriver'
    return CHROME_DRIVER

nohead_drivers = {}
def isBrowserOpened(username):
    if username in nohead_drivers.keys():
        pop_driver = nohead_drivers.pop(username)
        pop_driver.close()
        return True
    return False

def setBrowser(username, isMitmProxy):
    browser = None
    options = Options()
    # options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}
    # prefs = {"profile.managed_default_content_settings.images": 2, 'download.default_directory':os.getcwd()}
    options.add_experimental_option("prefs", prefs)
    if isMitmProxy:
        options.add_argument('--proxy-server=http://127.0.0.1:9000')
    options.add_argument('disable-infobars')
    options.add_argument('--no-sandbox')
    options.add_argument('--user-data-dir=./app/api/data_getter/userdata/' + username)
    CHROME_DRIVER = getChromeDriverDir()
    browser = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)
    nohead_drivers[username] = browser
    return browser
