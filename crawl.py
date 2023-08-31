### LIBRARY  ###
from selenium  import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import datetime
from typing import List
from puzzle import Puzzle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from puzzle import Puzzle
import re
from unidecode import unidecode
from post_tiktok_etractor import PostTikTokExtractor, PostCommentExtractor
import unicodedata
from utils.common_utils import CommonUtils
import config
import captcha
# from utils.format_time import format_time

options = webdriver.ChromeOptions()
# options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
# options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-save-password-bubble')
options.add_argument('--disable-translate')
# options.add_argument('--disable-web-security')
options.add_argument('--disable-extensions')

# driver = webdriver.Chrome(options=options)


class CrawlManage(object):
    XPATH_VIDEO_SEARCH = '//*[@class="tiktok-1soki6-DivItemContainerForSearch e19c29qe11"]'
    XPATH_VIDEO_OTHER = '//*[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe9"]'
    XPATH_VIDEO_USER ='//*[@data-e2e="user-post-item-desc"]' 
    
    def __init__(self, driver = webdriver.Chrome(options=options), config = config) -> None:
        self.driver = driver
        self.config = config
        self.option = self.config.option
    
    def parse_keyword(self) -> List[str]:
        keyword_list_raw_dict = []
        with open(self.config.keyword_path, "r", encoding='utf-8' ) as f:
            data = f.read()
            keyword_list_raw = json.loads(data)
            keyword_list_raw_dict = keyword_list_raw["keyword"]
        # for keyword_raw in keyword_list_raw:
        #     keyword_list_raw_dict.append(json.loads(keyword_raw))
        # # keyword_list_raw_dict = 
        keyword_list: List[str] = []
        # Lặp qua mỗi dict trong danh sách
        for item in keyword_list_raw_dict:
            # Lấy giá trị của key
            key = item['key']
            # Lặp qua mỗi giá trị trong subKey
            for subkey in item['subKey']:
                # Tạo từ khóa kết hợp từ key và subKey
                combined_keyword = f"{key} {subkey}"
                # Thêm từ khóa kết hợp vào danh sách keywords
                keyword_list.append(combined_keyword)
        return key, keyword_list
    
    def filter_post(self, content):
        check = 0
        keywork, keyword_list = self.parse_keyword()
        keyword_list.append(keywork)
        for key in keyword_list:
            key = key.lower()
            content = content.lower()
            key = unicodedata.normalize('NFKD', key).encode('ASCII', 'ignore').decode('utf-8')
            content = unicodedata.normalize('NFKD', content).encode('ASCII', 'ignore').decode('utf-8')
            if key in content:
                check = 1
                break
            else:
                hashtag = "#" + key.replace(" ", "")
                if hashtag in content:
                    check = 1
                    break
                else:
                    continue
        if check == 0:
            return False
        elif check == 1:
            return True
            
    def check_login_div(self):
        print("Check login div")
        try:
            button = self.driver.find_element(By.XPATH, '//*[@id="login-modal"]/div[2]')
            button.click()
        except:
            print("No login div")
        
    def crawl_comment(self, link):
        def scroll_comment():
            cmts=[]
            check = 1
            while((len(cmts) < 1000) & (len(cmts) != check) ):
                    # comments_section = self.driver.find_element(By.XPATH, '//*[@data-e2e="search-comment-container"]/div')
                    # actions.move_to_element(comments_section)
                check = len(cmts)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                cmts = self.driver.find_elements(By.XPATH, '//*[@class="tiktok-1i7ohvi-DivCommentItemContainer eo72wou0"]')
                time.sleep(3)
            try:
                self.driver.execute_script("window.scrollTo(0, 0);")
            except:
                pass
            return cmts
        
        try:
            list_cmt = scroll_comment()
            for cmt in list_cmt:
                comment_id = cmt.find_element(By.TAG_NAME, 'div').get_attribute('id')
                
                try: 
                        button = (cmt.find_element(By.XPATH, '//*[@data-e2e="comment-hide"]'))
                        button.click()
                except:
                        pass
                try:
                        div = cmt.find_elements(By.TAG_NAME, 'div')
                        count_reply = div[6].text
                        count_reply = int(self.extract_numbers_from_string(count_reply)[0])
                    # except Exception as e:
                    #     print(e)
                except:
                        count_reply = 0
                        
                    
                comment_extractor: PostCommentExtractor = PostCommentExtractor(driver=self.driver, link = link, post_id= comment_id, comment= count_reply)
                        # data[vid] = self.CrawlVideo(vid)
                comment = comment_extractor.extract()
                with open("result.txt", "a", encoding="utf-8") as file:
                    file.write(f"{str(comment)}\n")
                            # NguyenNH: in màu cho dễ debug
                    if comment.is_valid:
                        file.write(f"##################################################################################################################################################################################\n")
                    else:
                        file.write(f"🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈\n")
        except Exception as e:
            print(e)
    
    def run(self):
        count = 000
        self.driver.get("https://www.tiktok.com/")
        self.check_login_div()
        print("Start crawl")
        time.sleep(3)
        link_list = self.get_link_list()
        for link in link_list:
            self.driver.get(link)
            self.check_login_div()
            captcha.check_captcha(self.driver)
            if self.option == 'search_post':
                content = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-video-desc"]').text
                check = self.filter_post(content)
                if check:
                    pass
                else:
                    print(f"Filter out link {link}")
                    continue
            try: 
                with open('dataCrawled.txt', 'r') as f:
                    data_crawled = f.read()
                if link in data_crawled:
                    print("This video is crawled")
                    continue
                else:
                    print(f"Start crawl link : {link}")
                    start = time.time()
                        # data = {}
                    # self.driver.get(vid)
                    post_extractor: PostTikTokExtractor = PostTikTokExtractor(driver=self.driver, link = link)
                        # data[vid] = self.CrawlVideo(vid)
                    post = post_extractor.extract()
                    retry_time = 0
                    def retry_extract(post, retry_time):
                        while not post.is_valid():
                            post = post_extractor.extract()
                            if retry_time > 0:
                                print(f"Try to extract post {retry_time} times {str(post)}")
                                slept_time = CommonUtils.sleep_random_in_range(1, 5)
                                print(f"Slept {slept_time}")
                            retry_time = retry_time + 1
                            if retry_time > 20:
                                print("Retried 20 times, skip post")
                                break
                        return
                    retry_extract(post, retry_time)
                    
                    count += 1
                    with open('dataCrawled.txt', 'a') as f:
                        f.write(f"{link}\n")
                    with open("result.txt", "a", encoding="utf-8") as file:
                        file.write(f"{str(post)}\n")
                        if post.is_valid:
                            file.write(f"🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷\n")
                        else:
                            file.write(f"🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈\n")

            except Exception as e:
                print(e)
                    # print("count: ", count)
                pass
            try: 
                self.crawl_comment(link)
                end = time.time()
                print(f"Time for video {count}: ",end - start)
            except Exception as e:
                print(e)

    def scroll(self, xpath):
        vidList = []
        time.sleep(2)
        try:
            captcha.check_captcha(self.driver)
        except:
            pass
        count = 1
        vid_list_elem =[]
        while(len(vid_list_elem) != count and len(vid_list_elem) < self.config.count_of_vid):
                # data-e2e="search-common-link"
                count = len(vid_list_elem)
                try:
                    vid_list_elem = self.driver.find_elements(By.XPATH, xpath)
                except:
                    vid_list_elem = self.driver.find_elements(By.XPATH, xpath)
                # print("len vid: ", len(vid_list_elem))
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        time.sleep(3)
        for vid in vid_list_elem:
                    # print("###################################################")
                link = vid.find_element(By.TAG_NAME, 'a').get_attribute('href')
                
                vidList.append(link)
        print("Count of links: ", len(vidList))
        return vidList
        
    def get_link_list(self) -> list:
        print('-------> GET LINK LIST <-------')
        vidList=[]
        keywork, keyword_list = self.parse_keyword()
        if self.option == "search_post":
            self.driver.get(self.config.search_post_tiktok + keywork)
            # captcha.check_captcha(self.driver)
            vidList = self.scroll(xpath = self.XPATH_VIDEO_SEARCH)
        elif self.option == "search_user":
            self.driver.get(self.config.search_page_tiktok + self.config.user_id)
            vidList = self.scroll(xpath = self.XPATH_VIDEO_USER)
        elif self.option == "tag":
            self.driver.get(self.config.hashtag_tiktok + keywork)
            vidList = self.scroll(xpath = self.XPATH_VIDEO_OTHER)
        elif self.option == "explore":
            self.driver.get(self.config.explore_tiktok)
            div = self.driver.find_elements(By.XPATH, '//*[@id="main-content-explore_page"]/div/div[1]/div[1]/div')
            for d in div:
                if d.text == self.config.explore_option:
                    d.click()
                    break
            vidList = self.scroll(xpath = self.XPATH_VIDEO_OTHER)
        return vidList
            
    
        
        
        