from time import sleep

import pytest
import yaml
from appium import webdriver
from appium.webdriver.extensions.android.gsm import GsmCallActions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from hamcrest import *


class TestDemo:
    search_data = yaml.safe_load(open('search.yaml', 'r', encoding='utf8'))
    print(search_data)

    def setup(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "noblank"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["autoGrantPermissions"] = "true"
        caps["unicodeKeyboard"] = "true"
        caps["chromedriverExecutable"] = r"C:\Users\fengchuanyun\AppData\Local\Programs\Appium\resources\app\node_modules\appium\node_modules\appium-chromedriver\chromedriver\win\chromedriver.exe"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)  # 添加隐式等待

        # 如果出现升级弹框，先把弹框处理掉，以防影响用例执行；如果不出现，也不会影响用例执行

        # 方法1
        # if len(self.driver.find_elements_by_id("取消升级按钮")) > 0:
        #     self.driver.find_elements_by_id("取消升级按钮").click()

        # 方法2---显示等待，但是如果不出现的话，会报错
        # WebDriverWait(self.driver, 15).until(expected_conditions.visibility_of_element_located((By.ID, '取消升级按钮')))
        # self.driver.find_elements_by_id("取消升级按钮").click()

        # 方法3---显示等待(增强版)
        def loaded(driver):
            if len(self.driver.find_elements_by_id("取消升级按钮")) > 0:
                self.driver.find_elements_by_id("取消升级按钮").click()
                return True
            else:
                return False
        try:
            WebDriverWait(self.driver, 10).until(loaded)
        except Exception as e:
            print('没有出现升级弹框！', str(e))

    # 参数化1
    @pytest.mark.parametrize('keyword, expected_price', [('拼多多', 20), ('阿里巴巴', 100), ('京东', 10)])
    def test_search(self, keyword, expected_price):
        self.driver.find_element_by_id("com.xueqiu.android:id/tv_search").click()
        self.driver.find_element_by_id("com.xueqiu.android:id/search_input_text").send_keys(keyword)
        self.driver.find_element_by_id('name').click()
        price = self.driver.find_element_by_id("current_price")
        assert float(price.text) > expected_price
        assert 'com.xueqiu.android' == price.get_attribute('package')
        assert 'price' in price.get_attribute('resource-id')
        assert_that(price.get_attribute('package'), equal_to('com.xueqiu.android'))

    # 参数化2
    @pytest.mark.parametrize('keyword, expected_price', search_data)
    def test_search_from_search_yaml(self, keyword, expected_price):
        self.driver.find_element_by_id("com.xueqiu.android:id/tv_search").click()
        self.driver.find_element_by_id("com.xueqiu.android:id/search_input_text").send_keys(keyword)
        self.driver.find_element_by_id('name').click()
        price = self.driver.find_element_by_id("current_price")
        assert float(price.text) > expected_price
        assert 'com.xueqiu.android' == price.get_attribute('package')
        assert 'price' in price.get_attribute('resource-id')
        assert_that(price.get_attribute('package'), equal_to('com.xueqiu.android'))

    def test_search_from_test_case_yaml(self):
        TestCase('test_case.yaml').run(self.driver)

    def test_capabilities(self):
        self.driver.find_element_by_id("com.xueqiu.android:id/tv_search").click()
        self.driver.find_element_by_id("com.xueqiu.android:id/search_input_text").send_keys("阿里巴巴")

    def test_gsm_call(self):
        self.driver.make_gsm_call('18601931298', GsmCallActions.CALL)

    def test_send_sms(self):
        self.driver.send_sms('18601931298', 'Hey Jerry')

    def test_performance(self):
        print(self.driver.get_performance_data_types())
        for p in self.driver.get_performance_data_types():
            try:
                print(self.driver.get_performance_data('com.xueqiu.android', p, 5))
            except Exception as e:
                print('有错误', str(e))

    def test_xpath(self):
        # self.driver.find_element_by_xpath('//*[@text="关注"]').click()
        # self.driver.find_element_by_xpath('//*[contains(@resource-id,"iv_add_user")]').click()
        # self.driver.find_element_by_xpath('//*[contains(@index, 0) and contains(@text, "基金")]').click()
        self.driver.find_element_by_xpath('//*[@index=1 and @text="基金"]').click()

    # webview难点
    def test_webview_api_24(self):
        self.driver.find_element_by_xpath('//*[@text="交易"]').click()
        print(self.driver.contexts)
        self.driver.find_element_by_xpath('//*[@text="A股开户"]').click()
        print(self.driver.current_context)
        # 对于webview的页面，如果第一次无法定位，那么刷新uiautomatorviewer，便可定位了
        self.driver.switch_to.context(self.driver.contexts[-1])
        print(self.driver.current_context)
        WebDriverWait(self.driver, 15).until(expected_conditions.visibility_of_element_located((By.ID, 'phone-number')))
        self.driver.find_element_by_id('phone-number').send_keys('18601931298')

    def teardown(self):
        pass
        # self.driver.quit()


class TestCase:
    def __init__(self, path):
        file = open(path, 'r', encoding='utf8')
        self.steps = yaml.safe_load(file)

    def run(self, driver):
        for step in self.steps:
            element = None
            if isinstance(step, dict):
                if 'id' in step.keys():
                    element = driver.find_element_by_id(step['id'])
                elif 'xpath' in step.keys():
                    element = driver.find_element_by_xpath(step['xpath'])
                else:
                    print(step.keys())
                if 'input' in step.keys():
                    element.send_keys(step['input'])
                elif 'get' in step.keys():
                    text = element.get_attribute(step['get'])
                    if 'assert' in step.keys():
                        assert float(text) > step['assert']
                    else:
                        print(text)
                else:
                    element.click()
