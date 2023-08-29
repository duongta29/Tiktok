from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

options = webdriver.ChromeOptions()

options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-save-password-bubble')
options.add_argument('--disable-translate')
options.add_argument('--disable-web-security')
options.add_argument('--disable-extensions')

driver = webdriver.Chrome(options=options)
driver.get("https://www.tiktok.com/foryou")
# Đóng trình duyệt
driver.quit()