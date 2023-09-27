from appium import webdriver as webdriver_appium
import appium
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.keys import Keys
import time
import clipboard
import config

def perform_swipe(driver):
    deviceSize = driver.get_window_size()
    screenWidth = deviceSize['width']
    screenHeight = deviceSize['height']

    startx = screenWidth / 2
    endx = screenWidth / 2
    starty = screenHeight * 8 / 9
    endy = screenHeight / 9

    actions = TouchAction(driver)
    actions.long_press(None, startx, starty).move_to(None, endx, endy).release().perform()
    time.sleep(2)

def run_appium(keyword):
    desired_cap = {
        "uuid": "33005d5ad005c327 device",
        "platformName": "Android",
        "appPackage": "com.sec.android.app.launcher",
        "appActivity": "com.sec.android.app.launcher.activities.LauncherActivity"
    }

    link_list = []
    driver = webdriver_appium.Remote('http://localhost:4723/wd/hub', desired_cap)
    driver.implicitly_wait(30)

    perform_swipe(driver)
    time.sleep(1.5)
    button = driver.find_element("xpath", '//android.widget.FrameLayout[@content-desc="TikTok"]/android.widget.ImageView')
    button.click()
    time.sleep(3)
    driver.implicitly_wait(10)

    search_button = driver.find_element("id", 'com.ss.android.ugc.trill:id/d37')
    search_button.click()
    driver.implicitly_wait(10)
    search = driver.find_element("id", "com.ss.android.ugc.trill:id/cxz")

    search.send_keys(keyword)
    search = driver.find_element("id", "com.ss.android.ugc.trill:id/m_s")
    search.click()
    time.sleep(5)
    driver.implicitly_wait(10)

    filter_button = driver.find_element("id", "com.ss.android.ugc.trill:id/jbi")
    filter_button.click()
    fil = driver.find_element("id", 'com.ss.android.ugc.trill:id/b6z')
    fil.click()

    arrange_button = driver.find_element("xpath", '//android.widget.TextView[@index="3"]')
    arrange_button.click()
    apply_buton = driver.find_element("xpath", '//android.widget.Button[@content-desc="Áp dụng"]')
    apply_buton.click()
    time.sleep(3)
    video = driver.find_element("id", "com.ss.android.ugc.trill:id/mx0")
    video.click()
    return driver


def get_link():
    driver = run_appium()
    post = 0
    while post <= 100:
        share = driver.find_element("id", "com.ss.android.ugc.trill:id/jme")
        share.click()
        copy_link = driver.find_element("xpath", '//android.widget.Button[@content-desc="Sao chép Liên kết"]/android.widget.ImageView')
        copy_link.click()
        time.sleep(5)
        link = clipboard.paste()
        # link_list.append(link)
        with open("link_list_android.txt", "a") as f:
            f.write(f"{link}\n")
        perform_swipe(driver)
        post += 1

# run_appium("chung cu")