from appium import webdriver


class TestDemo:
    def setup(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "noblank"
        caps["autoGrantPermissions"] = "true"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["appPackage"] = "com.xueqiu.android"
        caps["unicodeKeyboard"] = "true"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)

    def test_demo(self):
        el1 = self.driver.find_element_by_id("com.xueqiu.android:id/tv_skip")
        el1.click()
        el2 = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.TextView")
        el2.click()
        el3 = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.EditText")
        el3.send_keys("alibaba")

    def test_capabilities(self):
        el1 = self.driver.find_element_by_id("com.xueqiu.android:id/tv_skip")
        el1.click()
        el2 = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.TextView")
        el2.click()
        el3 = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.EditText")
        el3.send_keys("阿里巴巴")

    def teardown(self):
        self.driver.quit()
