from datetime import date, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

from app.api.data_getter import nohead_browser

URL = 'https://kandianbao.com/?s=dsy_login'

class Login:

    def __init__(self, browser, account, password):
        self.browser = browser
        self.account = account
        self.password = password

    def is_element_exist(self, browser, cssSelector):
        try:
            browser.find_element_by_css_selector(cssSelector)
            return True
        except:
            return False
    
    def errorDetect(self):
        """ Detect whether account or password is wrong """
        accountError = self.browser.find_element_by_css_selector('#_account-noty')
        passwordError = self.browser.find_element_by_css_selector('#_password-noty')
        if accountError.get_attribute('style') == '':
            print(str(accountError.text))
            return -1
        if passwordError.get_attribute('style') == '':
            print(str(passwordError.text))
            return -1
        return 0

    def login(self):
        self.browser.get(URL)
        self.browser.find_element_by_css_selector("ul[class~='pull-right'] > li > a").click()
        try:
            account_input_element = self.browser.find_element_by_css_selector('#account')
        except NoSuchElementException:
            return None
        account_input_element.clear()
        account_input_element.send_keys(self.account)
        password_input_element = self.browser.find_element_by_css_selector('#password')
        password_input_element.click()
        password_input_element.clear()
        password_input_element.send_keys(self.password)
        if self.errorDetect() == -1:
            self.browser.close()
            return '账号或密码有误'
        password_input_element.send_keys(Keys.ENTER)
        if '登录' in self.browser.title:
            self.browser.close()
            return '密码格式错误，应为6-16位字母数字组合'
        return self.browser

# browser = nohead_browser.setBrowser('testuser2')
# Login(browser, '', '').login()
