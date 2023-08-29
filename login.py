from selenium  import webdriver
from time import sleep
import time
import pyotp
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import json
import pickle
options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920x1920")
# options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-notifications')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--lang=en-US')
#### GLOBAL INIT #####
url = 'https://www.tiktok.com/'
account = 'account.json'
# driver = webdriver.Chrome(executable_path ='chromedriver.exe')
# driver.get(url)
# sleep(3)


### CLASS ###

class TiktokLogin:
    def __init__(self, driver,account):
        self.driver = driver
        with open(account, 'r') as f:
            account = json.load(f)
        self.user = account['user']
        self.password = account['password']


    def loginTiktokwithPass(self):
        login = self.driver.find_element(By.XPATH, '//*[@id="header-login-button"]')
        login.click()
        time.sleep(3)
        log_email = self.driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div/div/a[2]/div')
        log_email.click()
        time.sleep(5)
        log = self.driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[2]/form/div[1]/a')
        log.click()
        time.sleep(3)
        user = self.driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[2]/form/div[1]/input')
        user.send_keys(self.user)
        password = self.driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[2]/form/div[2]/div/input')
        password.send_keys(self.password)
        button = self.driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div[2]/form/button')
        button.click()
        
        
    def save_cookie(self):
        self.loginTiktokwithPass
        cookies_list = self.driver.get_cookies()
        cookies_dict = {}

        for cookie in cookies_list:
            cookies_dict[cookie['name']] = cookie['value']

        # print("cookies_dict", cookies_dict)
        cookies = "Cookie: fr=" + cookies_dict.get('fr') + "; sb=" + cookies_dict.get('sb') + "; datr=" + cookies_dict.get('datr') + "; wd=" + cookies_dict.get(
            'wd') + "; c_user=" + cookies_dict.get('c_user') + "; xs=" + cookies_dict.get('xs')
        
        with open('cookies2.json', 'r') as f:
            data = json.load(f)
        data[self.user] = cookies
        with open('cookies2.json', 'w') as f:
            json.dump(data, f)
        self.driver.close()
        return cookies

        # pickle.dump(self.driver.get_cookies(), open("my_cookie.pkl","wb"))
        
    def loginTiktokwithCookie(self):
        with open('cookies2.json', 'r') as f:
            data = json.load(f)
        cookie = data.get('cookies', 'default_value')
        # script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://facebook.com"; })();'
        script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.tiktok.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://tiktok.com"; })();'
        self.driver.execute_script(script)
        
### DEFINE ###
# def crawl_group()
### MAIN ###
def main():
    driver = webdriver.Chrome(executable_path ='chromedriver.exe',options=options)
    driver.get(url)
    time.sleep(3)
    ttLogin = TiktokLogin(driver, account)
    # ttLogin.loginTiktokwithPass()
    # a = ttLogin.save_cookie()
    # with open ('cookies.json', 'r') as f:
    #     data = json.load(f)
    # data["cookies"] = a
    # with open ('cookies.json', 'w') as f:
    #     json.dump(data, f, indent=4)
        
    ttLogin.loginTiktokwithCookie()
    # time.sleep(200)
    # fbLogin.save_cookie
    # # fbLogin.loginFacebookwithCookie()
    # # driver.quit()
    # link = "https://www.facebook.com/groups/834058550598705"
    # driver.get(link)
    # time.sleep(100)
### EXECUTE ###
if __name__ == '__main__':
    main()

