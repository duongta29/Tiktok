### LIBRARY  ###
from selenium  import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
from login import TiktokLogin
from puzzle import Puzzle
import config

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-save-password-bubble')
options.add_argument('--disable-translate')
options.add_argument('--disable-web-security')
options.add_argument('--disable-extensions')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_argument("--log-level=3")
import captcha
driver = webdriver.Chrome(options=options)


#### GLOBAL INIT #####
url = 'https://www.tiktok.com/'
account = 'account.json'
driver.get(url)
time.sleep(3)
ttLogin = TiktokLogin(driver, username= "xinhxinh29")  
ttLogin.loginTiktokwithCookie()
actions = ActionChains(driver)
puzzle = Puzzle(driver)
# time.sleep(100)

### CLASS  ###
class Bot:
    def __init__(self):
        with open(config.config_path, "r") as f:
            choice = f.read()
            choice = json.loads(choice)
        self.action_choice = choice["mode"]["action"]
        self.key_comment = choice["mode"]["key_comment"]
        self.key = choice["mode"]["key"]
        self.type = choice["mode"]["type"]
        self.report_type = choice["mode"]["report_type"]
        self.count_post = choice["mode"]["count_post"]
 #       self.link = link
        
    def bot(self, action, link):
        driver.get(link)
        time.sleep(2)
        if action == 'comment' :
            return self.comment(self.key_comment)
        if action == 'like':
            return self.like()
        if action == 'share':
            return self.share()
        if action == 'follow':
            return self.follow()
        if action == 'report':
            return self.report()
        if action == 'love':
            return self.love()
        
    def comment(self):
        # driver.get(self.link)
        # time.sleep(2)
        button = driver.find_element(By.XPATH, '//*[@data-e2e="comment-icon"]')
        button.click()
        time.sleep(1)
        button = driver.find_element(By.XPATH, '//*[@role="textbox"]')
        # button.click()
        button.send_keys(self.key_comment)
        button.send_keys(Keys.ENTER)
        time.sleep(1)
    
    def love(self):
        try:
            check = driver.find_element(By.XPATH, '//*[@transform="matrix(1.000152826309204,0,0,1.000152826309204,23.990829467773438,30.984107971191406)"]')
            print(check)
            print('loved')
        except:
            check = driver.find_element(By.XPATH, '//*[@transform="matrix(1.0020687580108643,0,0,1.0020687580108643,23.875873565673828,30.78485107421875)"]')
            print('check')
            button = driver.find_element(By.XPATH, '//*[@data-e2e="undefined-icon"]')
            button.click()
        time.sleep(1)
        
    def like(self):
        # driver.get(self.link)matrix(1,0,0,1,0,0)
        # time.sleep(2)
        check = driver.find_element(By.XPATH, '//*[@data-e2e="like-icon"]/div/div')
        check = (check.find_elements(By.XPATH, '//*[@transform="matrix(1,0,0,1,0,0)"]'))[1]
        check= check.find_element(By.TAG_NAME, 'path')
        print(check.get_attribute('fill'))
        if check.get_attribute('fill') == "rgb(254,44,85)":
            print("liked")
        elif check.get_attribute('fill') == "rgb(255,255,255)":
            button = driver.find_element(By.XPATH, '//*[@data-e2e="like-icon"]')
            button.click()
            # button.click()
            time.sleep(1)
        
    def share(self):
        # driver.get(self.link)
        # time.sleep(2)
        button = driver.find_element(By.XPATH, '//*[@data-e2e="share-icon"]')
        actions.move_to_element(button)
        button.click()
        time.sleep(1.25)
        share_link = driver.find_element(By.ID, 'icon-element-copy')
        share_link.click()
        time.sleep(1)
    
    def follow(self):
        button = driver.find_element(By.XPATH, '//*[@data-e2e="browse-follow"]')
        check = button.text
        if check == "Follow":
            button.click()
        else:
            pass
        time.sleep(1)
        
    # def report(self):
    #     button = driver.find_element(By.XPATH, '//*[@fill="#fff"]')
    #     button.click()
        
    def get_link_video(self):
        
        print('GetLink')
        # time.sleep(5)
        url = f"https://www.tiktok.com/search/{self.type}?q={self.key}"
            # self.driver.get('https://www.google.com/')
            # time.sleep(8)
        driver.get(url)
            # self.SearchBox()
        time.sleep(3)
        try:
            captcha.check_captcha(driver)
            # return self.get_link_video()
        except:
            pass
        count = 1
        vidList=[]
        while(len(vidList) < self.count_post):
              #  count = len(vidList)
                # print('côunt',count)
                vidList=[]
                vid_elem = driver.find_elements(By.XPATH, '//*[@aria-label="Watch in full screen"]')
                for vid in vid_elem:
                    vid = vid.find_element(By.TAG_NAME, 'a')
                    vidList.append((vid.get_attribute('href')))
                print("len vid: ", len(vidList))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
        vidList = vidList
        return vidList
    
    def bot_list_vid(self):
        vidList = self.get_link_video()
        count = 1
        for vid in vidList:
            if count % 10 == 0:
                time.sleep(10)
            else:
                pass
            count += 1
            key = self.key
            action = self.action_choice
            print(action)
            self.bot(action=action, link=vid)
        
    def report(self):
        # driver.get(link)
        time.sleep(2)
        space = driver.find_element(By.XPATH, '//*[@id="xgwrapper-4-7266151702405893384"]/video')
        #actions.move_to_element(space)
        space.click()
        #time.sleep(1)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        button = driver.find_element(By.XPATH, '//*[@class="tiktok-1a3eiq7-DivRightControlsWrapper e1ya9dnw9"]/div[5]')
        actions.move_to_element(button)
        button.click()
        report = button.find_element(By.TAG_NAME, 'li')
        report.click()
        # return report_form(form)
        with open('report.json', 'r') as f:
            data = json.load(f)
        for key, value in data.items():
            if value == self.report_type:
                type_report = key
                # print("Khóa tìm thấy:", key)
                break
            elif isinstance(value, list) and self.report_type in value:
                type_report = key
                break
        time.sleep(2)
        elem_report = driver.find_element(By.XPATH, '//*[@data-e2e="report-form"]/div[2]')
        label = elem_report.find_elements(By.TAG_NAME, 'label')
            # //*[@id="tux-portal-container"]/div/div[2]/div/div/div[2]/div/div/section/form/div[2]/label[2]
        print("Text: ", len(label))
        
        for elem in label:
            # print(elem.text)
            if elem.text == type_report:
                print(elem.text)
                actions.move_to_element(elem).click(elem).perform()
                break
        
        try:
            elem_report = driver.find_element(By.XPATH, '//*[@data-e2e="report-form"]/div[2]')
            label = elem_report.find_elements(By.TAG_NAME, 'label')
            for elem in label:
                if elem.text == form:
                    actions.move_to_element(elem).click(elem).perform()
                    # actions.click(elem)
                    break
            button_submit = driver.find_element(By.XPATH,'//*[@data-e2e="report-form"]/div[2]/div[3]/button')
            button_submit.click()
        except:
            button_submit = driver.find_element(By.XPATH,'//*[@data-e2e="report-form"]/div[2]/div[3]/button')
            button_submit.click()

### TABLE OF REPORT

    ### Violence, abuse, and criminal exploitation
        ### Exploitation and abuse of people under 18
        ### Physical violence and violent threats
        ### Sexual exploitation and abuse 
        ### Human exploitation
        ### Animal abuse
        ### Other criminal activities
    ### Hate and harassment
        ### Hate speech and hateful behaviors
        ### Harassment and bullying
    ### Suicide and self-harm
    ### Disordered eating and unhealthy body image
    ### Dangerous activities and challenges
    ### Nudity and sexual content
        ### Youth sexual activity, solicitation, and exploitation
        ### Sexually suggestive behavior by youth
        ### Adult sexual activity, services, and solicitation
        ### Adult nudity
        ### Sexually explicit language
    ### Shocking and graphic content
    ### Misinformation
        ### Election misinformation
        ### Harmful misinformation
        ### Deepfakes, synthetic media, and manipulated media
    ### Deceptive behavior and spam
        ### Fake engagement
        ### Spam
        ### Undisclosed branded content
    ### Regulated goods and activities
        ### Gambling
        ### Alcohol, tobacco, and drugs
        ### Firearms and dangerous weapons
        ### Trade of other regulated goods and services
    ### Frauds and scams
    ### Sharing personal information
    ### Counterfeits and intellectual property
        ### Counterfeit products
        ### Intellectual property violation
    ### Other
    
    
# data = {}
# data["Violence, abuse, and criminal exploitation"] = ["Exploitation and abuse of people under 18","Physical violence and violent threats","Sexual exploitation and abuse"," Human exploitation","Animal abuse", "Other criminal activities"]
# data["Hate and harassment"] = ["Hate speech and hateful behaviors", "Harassment and bullying"]
# data["Suicide and self-harm"] = "Suicide and self-harm"
# data["Disordered eating and unhealthy body image"] = "Disordered eating and unhealthy body image"
# data["Dangerous activities and challenges"] = "Dangerous activities and challenges"
# data["Nudity and sexual content"] = ["Youth sexual activity, solicitation, and exploitation","Sexually suggestive behavior by youth","Adult sexual activity, services, and solicitation","Adult nudity","Sexually explicit language"]
# data["Shocking and graphic content"] = "Shocking and graphic content"
# data["Misinformation"] = ["Election misinformation","Harmful misinformation","Deepfakes, synthetic media, and manipulated media"]
# data["Deceptive behavior and spam"] = ["Fake engagement","Spam","Undisclosed branded content"]
# data["Regulated goods and activities"] = ["Gambling","Alcohol, tobacco, and drugs","Firearms and dangerous weapons","Trade of other regulated goods and services"]
# data["Frauds and scams"] = "Frauds and scams"
# data["Sharing personal information"] = "Sharing personal information"
# data["Counterfeits and intellectual property"] = ["Counterfeit products","Intellectual property violation"]
# data["Other"] = "Other"
# with open('report.json', 'w') as f:
#     json.dump(data, f, indent=4)

def main():
    bot = Bot()
    bot.bot_list_vid()
    
        
# def main():
#     action_choice = ['love','like', 'comment', 'share', 'follow']
#     # 'like', 'comment', 'share', 'follow'
#     keys = ['tuyệt vời', 'quá xịn', 'wow']
#     bot = Bot(action_choice, keys)
#     bot.BotVidList('video', 'marvel')
#     time.sleep(10)
    
    
main()
#    report('https://www.tiktok.com/@diem14122006/video/7266151702405893384?q=b%E1%BA%A1o%20l%E1%BB%B1c&t=1692672483144',form="Adult nudity")
