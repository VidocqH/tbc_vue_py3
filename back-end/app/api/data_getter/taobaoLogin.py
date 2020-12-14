import time
from datetime import date, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import platform

import os

TB_LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'

class Login:

    def __init__(self, account, password, browser):
        self.browser = None
        self.account = account
        self.password = password
        self.browser = browser

    def open(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(20)

    def start(self):
        # 1 初始化浏览器
        # self.init_browser(self.account)
        
        # 2 打开淘宝登录页
        self.browser.get(TB_LOGIN_URL)
        time.sleep(1)
        # 3 输入用户名
        self.write_username(self.account)
        time.sleep(1.5)
        # 4 输入密码
        self.write_password(self.password)
        time.sleep(1.5)
        # 5 如果有滑块 移动滑块
        if self.lock_exist():
            self.unlock()
        # 6 点击登录按钮
        self.submit()
        # 7 登录成功，直接请求页面
        # if self.is_element_exist('.login-error-msg'):
        #     errorMsg = str(self.browser.find_elements_by_css_selector('.login-error-msg.content > .content'))
        #     self.browser.close()
        #     return errorMsg
        # else:
        #     print("登录成功，跳转至目标页面")
        # errorMsg = str(self.browser.find_elements_by_css_selector('.login-error-msg.content > .content'))
        time.sleep(3.5)
        return self.browser

    def switch_to_password_mode(self):
        """
        切换到密码模式
        :return:
        """
        if self.browser.find_element_by_id('J_QRCodeLogin').is_displayed():
            self.browser.find_element_by_id('J_Quick2Static').click()

    def write_username(self, username):
        """
        输入账号
        :param username:
        :return:
        """
        try:
            username_input_element = self.browser.find_element_by_id('fm-login-id')
        except:
            username_input_element = self.browser.find_element_by_id('TPL_username_1')

        username_input_element.clear()
        username_input_element.send_keys(username)

    def write_password(self, password):
        """
        输入密码
        :param password:
        :return:
        """

        try:
            password_input_element = self.browser.find_element_by_id("fm-login-password")
        except:
            password_input_element = self.browser.find_element_by_id('TPL_password_1')

        #

        password_input_element.clear()
        password_input_element.send_keys(password)

    def lock_exist(self):
        """
        判断是否存在滑动验证
        :return:
        """
        return self.is_element_exist('#nc_1_wrapper') and self.browser.find_element_by_id(
            'nc_1_wrapper').is_displayed()

    def unlock(self):
        """
        执行滑动解锁
        :return:
        """
        if self.is_element_exist("#nocaptcha > div > span > a"):
            self.browser.find_element_by_css_selector("#nocaptcha > div > span > a").click()

        bar_element = self.browser.find_element_by_id('nc_1_n1z')
        ActionChains(self.browser).drag_and_drop_by_offset(bar_element, 258, 0).perform()
        if self.is_element_exist("#nocaptcha > div > span > a"):
            self.unlock()
        time.sleep(0.5)

    def submit(self):
        """
        提交登录
        :return:
        """
        try:
            self.browser.find_element_by_css_selector("#login-form > div.fm-btn > button").click()
        except:
            self.browser.find_element_by_id('J_SubmitStatic').click()

        time.sleep(0.5)
        if self.is_element_exist("#J_Message"):
            self.write_password(self.password)
            self.submit()
            time.sleep(5)

    def navigate_to_target_page(self):
        pass

    # def init_date(self):
    #     date_offset = 0
    #     self.today_date = (date.today() + timedelta(days=-date_offset)).strftime("%Y-%m-%d")
    #     self.yesterday_date = (date.today() + timedelta(days=-date_offset-1)).strftime("%Y-%m-%d")

    def init_browser(self, username):
        self.downloadPath = os.getcwd()
        CHROME_DRIVER = os.path.abspath(os.path.dirname(os.getcwd())) + os.sep + 'chromedriver' + os.sep
        if platform.system() == 'Windows':
            CHROME_DRIVER = os.getcwd() + os.sep + 'src\chromedriver.exe'
        if platform.system() == 'Linux':
            CHROME_DRIVER = os.getcwd() + os.sep + 'src/chromedriver'
        if platform.system() == 'Darwin':
            CHROME_DRIVER = os.getcwd() + os.sep + 'src/chromedriver'

        """
        初始化selenium浏览器
        :return:
        """
        options = Options()
        # options.add_argument("--headless")
        # prefs = {"profile.managed_default_content_settings.images": 2}
        prefs = {"profile.managed_default_content_settings.images": 2, 'download.default_directory': self.downloadPath}
        # 1是加载图片，2是不加载图片
        options.add_experimental_option("prefs", prefs)
        # options.add_argument('--proxy-server=http://127.0.0.1:9000')
        options.add_argument('disable-infobars')
        options.add_argument('--no-sandbox')
        options.add_argument('--user-data-dir=./src/userdata/' + username)
        self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)
        self.browser.implicitly_wait(3)
        self.browser.maximize_window()

    def is_element_exist(self, selector):
        """
        检查是否存在指定元素
        :param selector:
        :return:
        """
        try:
            self.browser.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False

# account = ''
# 输入你的账号名
# password = ''
# 输入你密码
# Login(account,password).start()

# lo = Login(account=account, password=password)
# lo.start()