### LIBRARY  ###
from selenium  import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import datetime
from puzzle import Puzzle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


### Option driver ###
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
driver = webdriver.Chrome(options=options)

### GLOBAL INIT ###
captcha = Puzzle(driver)


### CLASS ###
class Post:
    def __init__(self):
        self.id = ""
        # self.type = ""
        self.time_crawl = ""
        self.link = "https://www.tiktok.com/@thanhthao15.03/video/7255638157528485126"
        self.author = ""
        self.author_link = ""
        self.avatar = ""
        self.created_time = ""
        self.content = ""
        # self.image_url = []
        self.like = 0
        self.comment = 0
        # self.haha = 0
        # self.wow = 0
        # self.sad = 0
        self.love = 0
        # self.angry = 0
        self.share = 0
        self.domain = ""
        self.hastag = []
        self.music = ""
        # self.title = ""
        self.duration = 0
        self.view = 0
        # self.description = ""
        # self.video = ""
        self.source_id = ""
        
    #Hàm xác định xem post được crawl đủ hay chưa
    def is_valid(self) -> bool:
        is_valid = self.id != "" and self.author != "" and self.link != "" and self.created_time 
        return is_valid

    def __str__(self) -> str:
        string = ""
        for attr_name, attr_value in self.__dict__.items():
            string =  f"{attr_name}={attr_value}\n" + string
        return string
    
    def crawl_post(self):
        driver.get(self.link)
        time.sleep(2)
        try:
            button = driver.find_element(By.XPATH, '//*[@id="login-modal"]/div[2]')
            button.click()
            time.sleep(2)
        except:
            pass
        
        # crawl #
        getIDvid = driver.find_element(By.XPATH, '//*[@class="tiktok-web-player no-controls"]')
        self.id = ((getIDvid.get_attribute('id')).split('-'))[2]
        time_crawl = datetime.datetime.now()
        self.time_crawl = time_crawl.strftime("%Y-%m-%d %H:%M:%S")
        self.author = driver.find_element(By.XPATH, '//*[@data-e2e="browser-nickname"]/span[1]').text
        self.author_link = driver.find_element(By.XPATH, '//*[@data-e2e="browse-user-avatar"]').get_attribute('href')
        self.avatar = driver.find_element(By.XPATH, '//*[@data-e2e="browse-user-avatar"]/div/span/img').get_attribute('src')
        
        infor_text = driver.find_element(By.XPATH,'//*[@id="SIGI_STATE"]').get_attribute('text')
        infor_text = json.loads(infor_text)
        createTime = infor_text["ItemModule"][self.id]["createTime"]
        timestamp = int(createTime)  # Example Unix timestamp
        self.created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        self.content = driver.find_element(By.XPATH, '//*[@data-e2e="browse-video-desc"]').text 
        self.like = int(infor_text["ItemModule"][self.id]["stats"]["diggCount"])
        self.comment = int(infor_text["ItemModule"][self.id]["stats"]["commentCount"])
        self.love = int(infor_text["ItemModule"][self.id]["stats"]["collectCount"])
        self.share = int(infor_text["ItemModule"][self.id]["stats"]["shareCount"])
        self.domain = "www.tiktok.com"
        hastag = driver.find_elements(By.XPATH, '//*[@data-e2e="browse-video-desc"]/a')
        self.hastag = [elem.text for elem in hastag]
        self.music = driver.find_element(By.XPATH, '//*[@data-e2e="browse-music"]/a').get_attribute('href')
        self.duration = int(infor_text["ItemModule"][self.id]["video"]["duration"])
        self.view = int(infor_text["ItemModule"][self.id]["stats"]["playCount"])
        self.source_id = self.id
        self.is_valid
        return self.__str__
    
class Comment:
    def __init__(self):
        self.id = ""
        # self.type = ""
        self.time_crawl = ""
        self.link = "https://www.tiktok.com/@thanhthao15.03/video/7255638157528485126"
        self.author = ""
        self.author_link = ""
        self.avatar = ""
        self.created_time = ""
        self.content = ""
        # self.image_url = []
        self.like = 0
        self.comment = 0
        # self.haha = 0
        # self.wow = 0
        # self.sad = 0
        self.love = 0
        # self.angry = 0
        self.share = 0
        self.domain = ""
        self.hastag = []
        self.music = ""
        # self.title = ""
        self.duration = 0
        self.view = 0
        # self.description = ""
        # self.video = ""
        self.source_id = ""
    
    
        
def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

def write_to_json(post, filename):
    with open(filename, 'w') as f:
        json.dump(post.__dict__, f, indent=4, default=default_serializer)     
        
def main():
    driver.get("https://www.tiktok.com")
    time.sleep(3)
    try:
        button = driver.find_element(By.XPATH, '//*[@id="login-modal"]/div[2]')
        button.click()
    except:
        print("No login div")
    # time.sleep()
    try:
        print("Check Captcha")
        driver.find_element(By.XPATH, '//*[@id="captcha-verify-image"]')
        # driver.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div')
        captcha.puzzleSolver()
    except:
        print("No captcha")
    
    print("CRAWLING ........")
    post = Post()
    post.crawl_post()
    # with open("new.json", 'w') as f:
    #     f.write(data)
    write_to_json(post, 'new.json')
        
### EXECUTE ###
if __name__ == '__main__':
    main()

    
