# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver

caps = {}
caps["platformName"] = "android"
caps["deviceName"] = "noblank"
caps["autoGrantPermissions"] = "true"
caps["appActivity"] = ".view.WelcomeActivityAlias"
caps["appPackage"] = "com.xueqiu.android"

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
driver.implicitly_wait(10)

el1 = driver.find_element_by_id("com.xueqiu.android:id/tv_skip")
el1.click()

el2 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.TextView")
el2.click()
el3 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.EditText")
el3.send_keys("alibaba")

driver.quit()
