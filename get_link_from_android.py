from appium import webdriver
# from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.keys import Keys
# from appium.webdriver.common.keyevent import KeyEvent
import time
import clipboard


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

desired_cap ={
    "uuid": "127.0.0.1:62025 device",
    "platformName" : "Android",
    "appPackage" : "com.android.launcher3",
    "appActivity" :"com.android.launcher3.launcher3.Launcher"
    #adb shell dumpsys window | find "mCurrentFocus"
}
link_list = []
driver = webdriver.Remote('http://localhost:4720/wd/hub', desired_cap)
driver.implicitly_wait(30)

button = driver.find_element("xpath", '//android.widget.TextView[@content-desc="TikTok"]')
button.click()

# time.sleep(5)
driver.implicitly_wait(10)
# driver.implicitly_wait(30)
search_button = driver.find_element("xpath", '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/X.YAD/android.widget.TabHost/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView')
search_button.click()
driver.implicitly_wait(10)
search = driver.find_element("id", "com.ss.android.ugc.trill:id/cvx")

search.send_keys("chuyen bay giai cuu")
# search.send_keys(Keys.RETURN)
search = driver.find_element("id", "com.ss.android.ugc.trill:id/m3t")
search.click()
# driver.press_keycode(66)
time.sleep(5)
driver.implicitly_wait(10)

filter_button = driver.find_element("id", "com.ss.android.ugc.trill:id/j80")
filter_button.click()
fil = driver.find_element("id", 'com.ss.android.ugc.trill:id/b5p')
fil.click()

arrange_button = driver.find_element("xpath",'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.TextView[3]')
arrange_button.click()
# twenty_four = driver.find_element("xpath", "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.TextView[5]")
# twenty_four.click()
# //android.widget.Button[@content-desc="Áp dụng"]
apply_buton = driver.find_element("xpath", '//android.widget.Button[@content-desc="Áp dụng"]')
apply_buton.click()
video = driver.find_element("id", "com.ss.android.ugc.trill:id/j8a")
video.click()


post = 0
while (post <= 100):
    share = driver.find_element("id", "com.ss.android.ugc.trill:id/jh5")
    share.click()

    copy_link = driver.find_element("xpath", '//android.widget.Button[@content-desc="Sao chép Liên kết"]/android.widget.ImageView')
    copy_link.click()
    time.sleep(5)
    link = clipboard.paste()
    link_list.append(link)
    with open("link_list_android.txt", "a") as f:
        f.write(f"{link}\n")
    perform_swipe(driver)
    post += 1
    
