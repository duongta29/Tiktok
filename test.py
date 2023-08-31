### LIBRARY  ###
from selenium  import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import json
import pickle
from login import TiktokLogin
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from puzzle import Puzzle
from bot import Bot


options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
# options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
# options.add_argument('--disable-popup-blocking')
# options.add_argument('--disable-save-password-bubble')
# options.add_argument('--disable-translate')
# options.add_argument('--disable-web-security')
# options.add_argument('--disable-extensions')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)


#### GLOBAL INIT #####
url = 'https://www.tiktok.com/'
account = 'account.json'
driver.get(url)
time.sleep(3)
ttLogin = TiktokLogin(driver, account)  
ttLogin.loginTiktokwithCookie()
actions = ActionChains(driver)
# time.sleep(100)
bot = Bot()