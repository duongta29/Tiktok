### LIBRARY  ###
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import pickle
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
import ast
from get_link_from_android import *
# import kafka

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=["10.11.101.129:9092"])

# from utils.format_time import format_time

options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
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
# driver = webdriver.Chrome(options=options)


class CrawlManage(object):
    XPATH_VIDEO_SEARCH = '//*[contains(@class, "DivItemContainerForSearch")]'
    XPATH_VIDEO_OTHER = '//*[contains(@class, "DivItemContainerV2")]'
    # XPATH_VIDEO_OTHER = '//*[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe9"]'
    XPATH_VIDEO_USER = '//*[@data-e2e="user-post-item-desc"]'

    def __init__(self, driver=webdriver.Chrome(options=options), config=config) -> None:
        self.driver = driver
        self.config = config
        with open(self.config.config_path, "r", encoding='latin-1') as f:
            data = f.read()
            data = json.loads(data)
        self.option = data["mode"]["name"]

    def parse_keyword(self) -> List[str]:
        keyword_list_raw_dict = []
        keyword_list: List[str] = []
        with open(self.config.config_path, "r", encoding='utf-8') as f:
            data = f.read()
            keyword_list_raw = json.loads(data)
            keyword_list_raw_dict = keyword_list_raw["mode"]["keyword"]
            # options = keyword_list_raw["mode"]["name"]
        try:
            # keyword_list_raw_dict = json.loads(keyword_list_raw_dict)
            # Lặp qua mỗi dict trong danh sách
            for item in keyword_list_raw_dict:
                # item = json.loads(item)
                keywords = []
                # Lấy giá trị của key
                key = item['key']
                keywords.append(key)
                # key_list.append(key)
                # Lặp qua mỗi giá trị trong subKey
                for subkey in item['subKey']:
                    # Tạo từ khóa kết hợp từ key và subKey
                    combined_keyword = f"{key} {subkey}"
                    # Thêm từ khóa kết hợp vào danh sách keywords
                    keywords.append(subkey)
                    keywords.append(combined_keyword)
                keyword_list.append(keywords)
        except Exception as e:
            # print(e)
            keyword_list = [[item] for item in keyword_list_raw_dict]
        return keyword_list

    def filter_post(self, content, keyword_list):
        check = 0
        main_key = keyword_list[0].lower()
        accented_hashtags = "#" + main_key.replace(" ", "")
        content = content.lower()
        main_key = unicodedata.normalize('NFKD', main_key).encode(
                'ASCII', 'ignore').decode('utf-8')
        content = unicodedata.normalize('NFKD', content).encode(
                'ASCII', 'ignore').decode('utf-8')
        hashtag = "#" + main_key.replace(" ", "")
        if (main_key in content) or (hashtag in content) or (accented_hashtags in content):
            keyword_list.pop(0) 
            for key in keyword_list:
                key = key.lower()
                key = unicodedata.normalize('NFKD', key).encode(
                    'ASCII', 'ignore').decode('utf-8')
                if key in content:
                    check = 1
                    break
                else:
                    accented_hashtags = "#" + key.replace(" ", "")
                    hashtag = "#" + key.replace(" ", "")
                    if (hashtag in content) or (accented_hashtags in content):
                        check = 1
                        break
                    else:
                        continue
            if check == 0:
                return False
            elif check == 1:
                return True
        else: 
            return False

    def check_login_div(self):
        print("Check login div")
        try:
            button = self.driver.find_element(
                By.XPATH, '//*[@id="login-modal"]/div[2]')
            button.click()
        except:
            print("No login div")

    def extract_numbers_from_string(self, string):
        pattern = r'\d+'
        numbers = re.findall(pattern, string)
        number = int(numbers[0])
        return number

    def crawl_comment(self, link):
        comments = []

        def scroll_comment():
            cmts = []
            check = 1
            while((len(cmts) < 100) & (len(cmts) != check)):
                # comments_section = self.driver.find_element(By.XPATH, '//*[@data-e2e="search-comment-container"]/div')
                # actions.move_to_element(comments_section)
                check = len(cmts)
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                cmts = self.driver.find_elements(
                    By.XPATH, '//*[contains(@class, "DivCommentItemContainer")]')
                time.sleep(2)
            try:
                self.driver.execute_script("window.scrollTo(0, 0);")
            except:
                pass
            try:
                buttons = (self.driver.find_elements(
                    By.XPATH, '//*[@data-e2e="comment-hide"]'))
                for button in buttons:
                    button.click()
                    time.sleep(0.1)
            except:
                pass
            return cmts

        try:
            list_cmt = scroll_comment()
            print(">>> Crawling comment of post ...")
            for cmt in list_cmt:
                comment_id = cmt.find_element(
                    By.TAG_NAME, 'div').get_attribute('id')
                try:
                    div = cmt.find_elements(By.TAG_NAME, 'div')
                    count_reply = div[6].text
                    # count_reply = int(self.extract_numbers_from_string(count_reply)[0])
                    count_reply = self.extract_numbers_from_string(count_reply)
                except:
                    count_reply = 0
                comment_extractor: PostCommentExtractor = PostCommentExtractor(
                    driver=self.driver, link=link, post_id=comment_id, comment=count_reply)
                # data[vid] = self.CrawlVideo(vid)
                comment = comment_extractor.extract()
                comments.append(comment)
                with open("result.txt", "a", encoding="utf-8") as file:
                    file.write(f"{str(comment)}\n")
                    # NguyenNH: in màu cho dễ debug
                    if comment.is_valid:
                        file.write(
                            f"##################################################################################################################################################################################\n")
                    else:
                        file.write(
                            f"🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈\n")
        except Exception as e:
            print(e)
        return comments

    def crawl_post(self, link, keyword_list):
        posts = []
        check=False
        self.driver.get(link)
        self.driver.implicitly_wait(5)
        self.check_login_div()
        # time.sleep(30)
        print(f" >>> Crawling: {link} ...")
        captcha.check_captcha(self.driver)
        try:
            if self.option == 'search_post':
                content = self.driver.find_element(
                    By.XPATH, '//*[@data-e2e="browse-video-desc"]').text
                check = self.filter_post(content, keyword_list)
            if check or self.option != "search_post":
                    post_extractor: PostTikTokExtractor = PostTikTokExtractor(
                        driver=self.driver, link=link)
                    # data[vid] = self.CrawlVideo(vid)
                    post = post_extractor.extract()
                    retry_time = 0

                    def retry_extract(post, retry_time):
                        while not post.is_valid():
                            post = post_extractor.extract()
                            if retry_time > 0:
                                print(
                                    f"Try to extract post {retry_time} times {str(post)}")
                                slept_time = CommonUtils.sleep_random_in_range(1, 5)
                                print(f"Slept {slept_time}")
                            retry_time = retry_time + 1
                            if retry_time > 20:
                                print("Retried 20 times, skip post")
                                break
                        return
                    retry_extract(post, retry_time)
                    posts.append(post)
                    with open('dataCrawled.txt', 'a') as f:
                        f.write(f"{link}\n")
                    with open("result.txt", "a", encoding="utf-8") as file:
                        file.write(f"{str(post)}\n")
                        if post.is_valid:
                            file.write(f"🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷\n")
                        else:
                            file.write(
                                f"🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈\n")
                    return posts
            else:
                    print(f"Filter out link {link}")
                    return []
        except Exception as e:
            print(e)
                    


    def push_kafka(self, posts, comments):
        if len(posts) > 0:
            bytes_obj = pickle.dumps([ob.__dict__ for ob in posts])
            producer.send('lnmxh', bytes_obj)
            if len(comments) > 0:
                bytes_obj = pickle.dumps([ob.__dict__ for ob in comments])
                producer.send('lnmxh', bytes_obj)
            return 1
        else:
            return 0

    def run(self):
        posts = []
        count = 0
        self.driver.get("https://www.tiktok.com/")
        self.check_login_div()
        print("Start crawl")
        # time.sleep(3)
        keywords = self.parse_keyword()
        for keyword in keywords:
            link_list = self.get_link_list(keyword[0])
            for link in link_list:
                count += 1
                start = time.time()
                posts = self.crawl_post(link, keyword)
                if len(posts) != 0:
                    try:
                        comments = self.crawl_comment(link)
                        self.push_kafka(posts=posts, comments=comments)
                        end = time.time()
                        print(f"Time for video {count}: ", end - start)
                    except Exception as e:
                        print(e)
        time.sleep(30*60)
        return self.run()

    def scroll(self, xpath):
        vidList = []
        time.sleep(3)
        # self.driver.implicitly_wait(2)
        try:
            captcha.check_captcha(self.driver)
        except:
            pass
        count = 1
        vid_list_elem = []
        while(len(vid_list_elem) != count and len(vid_list_elem) < self.config.count_of_vid):
            # data-e2e="search-common-link"
            count = len(vid_list_elem)
            try:
                vid_list_elem = self.driver.find_elements(By.XPATH, xpath)
            except:
                vid_list_elem = self.driver.find_elements(By.XPATH, xpath)
            # print("len vid: ", len(vid_list_elem))
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        # time.sleep(3)
        for vid in vid_list_elem:
            link = vid.find_element(By.TAG_NAME, 'a').get_attribute('href')
            vidList.append(link)
        if len(vidList) == 0:
            print("Something went wrong")
            self.driver.refresh()
            return self.scroll(xpath)
        print("Count of links: ", len(vidList))
        with open('dataCrawled.txt', 'r') as f:
            data_crawled = f.read()
        for vid in vidList:
            if vid in data_crawled:
                vidList.remove(vid)
        return vidList

    def get_link_list(self, keyword) -> list:
        print('-------> GET LINK LIST <-------')
        vidList = []
        # keyword_dict, option = self.parse_keyword()
        if self.option == "search_post":
            self.driver.get(self.config.search_post_tiktok + keyword)
            # captcha.check_captcha(self.driver)
            vidList = self.scroll(xpath=self.XPATH_VIDEO_SEARCH)
        if self.option == "search_post_android":

            driver_appium = run_appium(keyword)
            post = 0
            link = None
            while post <= 3:
                share = driver_appium.find_element(
                    "id", "com.ss.android.ugc.trill:id/jme")
                share.click()
                copy_link = driver_appium.find_element(
                    "xpath", '//android.widget.Button[@content-desc="Sao chép Liên kết"]/android.widget.ImageView')
                copy_link.click()
                link_old = link
                link = clipboard.paste()
                # while link_old == link:
                #     time.sleep(1)
                time.sleep(5)
                self.driver.get(link)
                vid = self.driver.find_element(
                    By.XPATH, '//meta[@property="og:url"]').get_attribute("content")
                vidList.append(vid)
                # link_list.append(link)
                # with open("link_list_android.txt", "a") as f:
                #     f.write(f"{link}\n")
                perform_swipe(driver_appium)
                post += 1
                # with open("link_list_android.txt", "r") as f:
                #     vidList = [line.strip() for line in f.readlines()]
        elif self.option == "search_user":
            self.driver.get(self.config.search_page_tiktok +
                            self.config.user_id)
            # captcha.check_captcha(self.driver)
            vidList = self.scroll(xpath=self.XPATH_VIDEO_USER)
        elif self.option == "tag":
            self.driver.get(self.config.hashtag_tiktok + keyword)
            # captcha.check_captcha(self.driver)
            vidList = self.scroll(xpath=self.XPATH_VIDEO_OTHER)
        elif self.option == "explore":
            self.driver.get(self.config.explore_tiktok)
            # captcha.check_captcha(self.driver)
            div = self.driver.find_elements(
                By.XPATH, '//*[@id="main-content-explore_page"]/div/div[1]/div[1]/div')
            for d in div:
                if d.text == self.config.explore_option:
                    d.click()
                    break
            vidList = self.scroll(xpath=self.XPATH_VIDEO_OTHER)
        return vidList
