from appium import webdriver


class TestDemo:
    def setup(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "noblank"
        caps["appPackage"] = "com.example.android.apis"
        caps["appActivity"] = ".ApiDemos"
        caps["autoGrantPermissions"] = "true"
        caps["unicodeKeyboard"] = "true"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)  # 添加隐式等待

    def test_toast(self):
        self.driver.find_element_by_xpath('//*[@text="Views"]').click()
        self.driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("Popup Menu").instance(0));').click()
        self.driver.find_element_by_xpath('//*[@text="MAKE A POPUP!"]').click()
        assert len(self.driver.find_elements_by_xpath('//*[@text="Add"]')) == 1
        self.driver.find_element_by_xpath('//*[@text="Search"]').click()
        assert 'Clicked popup menu item Search' == self.driver.find_element_by_xpath('//*[@class="android.widget.Toast"]').text

    def teardown(self):
        self.driver.quit()
