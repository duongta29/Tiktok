import datetime
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from post_extractor import PostExtractor
# from utils.datetime_utils import DatetimeUtils
# from utils.log_utils import logger
# from utils.string_utils import StringUtils
import json
import re
import time
import traceback
from post_model import Post
from utils.format_time import format_time
# from selenium_utils import SeleniumUtils


class PostTikTokExtractor(PostExtractor):
    # POST_AUTHOR_XPATH: str = './/a[not(contains(@href, "group")) and not(@href="#")]'
    def __init__(self, driver: WebDriver, link):
        super().__init__(driver=driver)
        getIDvid = self.driver.find_element(
            By.XPATH, '//*[@class="tiktok-web-player no-controls"]')
        id = ((getIDvid.get_attribute('id')).split('-'))[2]
        self.id = id
        try:
            infor_text = self.driver.find_element(
                By.XPATH, '//*[@id="__UNIVERSAL_DATA_FOR_REHYDRATION__"]').get_attribute('text')
            infor_text = json.loads(infor_text)
            infor_text = infor_text["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]

        except:
            infor_text = self.driver.find_element(
                By.XPATH, '//*[@id="SIGI_STATE"]').get_attribute('text')
            infor_text = json.loads(infor_text)
            infor_text = infor_text["ItemModule"][self.id]
        self.infor_text = infor_text
        self.link = link

    def extract_post_link(self):
        return self.link

    def extract_post_id(self):
        id = "tt_" + self.id
        return id

    def extract_post_time_crawl(self):
        time_crawl = datetime.datetime.now()
        time_crawl = time_crawl.timestamp()
        return time_crawl

    def extract_post_author(self):
        author = self.driver.find_element(By.XPATH, '//*[@data-e2e="browser-nickname"]/span').text
        return author

    def extract_post_author_link(self):
        author_link = self.driver.find_element(
            By.XPATH, '//*[@data-e2e="browse-user-avatar"]').get_attribute('href')
        return author_link

    def extract_post_author_avatar(self):
        avatar = self.driver.find_element(
            By.XPATH, '//*[@data-e2e="browse-user-avatar"]').find_element(By.TAG_NAME, 'img')
        avatar = avatar.get_attribute('src')
        return avatar

    def extract_post_created_time(self):
        createTime = self.infor_text["createTime"]
        created_time = int(createTime)  # Example Unix timestamp
        # created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        return created_time

    def extract_post_content(self):
        return ""
    
    def extract_post_title(self):
        title = self.driver.find_element(
            By.XPATH, '//*[@data-e2e="browse-video-desc"]').text
        return title

    def extract_post_like(self):
        like = int(self.infor_text["stats"]["diggCount"])
        return like

    def extract_post_love(self):
        love = int(self.infor_text["stats"]["collectCount"])
        return love

    def extract_post_comment(self):
        comment = int(self.infor_text["stats"]["commentCount"])
        return comment

    def extract_post_share(self):
        share = int(self.infor_text["stats"]["shareCount"])
        return share

    def extract_post_domain(self):
        domain = "www.tiktok.com"
        return domain

    def extract_post_hagtag(self):
        hastag = self.driver.find_elements(
            By.XPATH, '//*[@data-e2e="browse-video-desc"]/a')
        hastag = [elem.text for elem in hastag]
        return hastag

    def extract_post_music(self):
        music = self.driver.find_element(
            By.XPATH, '//*[@data-e2e="browse-music"]/a').get_attribute('href')
        return music

    def extract_post_duration(self):
        duration = int(self.infor_text["video"]["duration"])
        return duration

    def extract_post_view(self):
        view = int(self.infor_text["stats"]["playCount"])
        return view

    def extract_post_type(self):
        type = "tiktok video"
        return type

    def extract_post_source_id(self):
        source_id = ""
        return source_id


class PostCommentExtractor(PostExtractor):
    # POST_AUTHOR_XPATH: str = './/a[not(contains(@href, "group")) and not(@href="#")]'
    def __init__(self, driver: WebDriver, link, post_id, comment):
        super().__init__(driver=driver)
        self.link = link
        self.post_id = post_id
        self.comment = comment
        # self.source_id = source_id

        # infor_text = self.driver.find_element(By.XPATH,'//*[@id="SIGI_STATE"]').get_attribute('text')
        # infor_text = json.loads(infor_text)
        # self.infor_text = infor_text

    def extract_post_link(self):
        return ""

    def extract_post_id(self):
        id = "tt_" + self.post_id
        return id

    def extract_post_time_crawl(self):
        time_crawl = datetime.datetime.now()
        time_crawl = time_crawl.timestamp()
        return time_crawl

    def extract_post_author(self):
        author = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/div[1]/a/span').text
        return author
    
    def extract_post_title(self):
        return ""

    def extract_post_author_link(self):
        author_link = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/a').get_attribute('href')
        return author_link

    def extract_post_author_avatar(self):
        avatar = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/a/span/img').get_attribute('src')
        return avatar

    def extract_post_created_time(self):
        createTime = self.driver.find_element(By.XPATH, f'//*[@id={self.post_id}]/div[1]/p[2]/span[1]').text
        createTime = format_time(createTime)
        return createTime

    def extract_post_content(self):
        content = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/div[1]/p[1]').text
        return content

    def extract_post_like(self):
        like = int(self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/div[1]/p[2]/div/span').text)
        return like

    def extract_post_love(self):
        return 0

    def extract_post_comment(self):
        comment = self.comment
        return comment

    def extract_post_share(self):
        return 0

    def extract_post_domain(self):
        domain = "www.tiktok.com"
        return domain

    def extract_post_hagtag(self):
        return ""

    def extract_post_music(self):
        return ""

    def extract_post_duration(self):
        return 0

    def extract_post_view(self):
        return 0

    def extract_post_type(self):
        type = "tiktok comment"
        return type

    def extract_post_source_id(self):
        getIDvid = self.driver.find_element(
            By.XPATH, '//*[@class="tiktok-web-player no-controls"]')
        source_id = "tt_" + ((getIDvid.get_attribute('id')).split('-'))[2]
        return source_id

class PostReplyExtractor(PostExtractor):
    # POST_AUTHOR_XPATH: str = './/a[not(contains(@href, "group")) and not(@href="#")]'
    def __init__(self, driver: WebDriver,source_id, post_id):
        super().__init__(driver=driver)
        self.post_id = post_id
        self.source_id = source_id

        # infor_text = self.driver.find_element(By.XPATH,'//*[@id="SIGI_STATE"]').get_attribute('text')
        # infor_text = json.loads(infor_text)
        # self.infor_text = infor_text

    def extract_post_link(self):
        return ""

    def extract_post_id(self):
        id = "tt_" + self.source_id + "." + self.post_id
        return id

    def extract_post_time_crawl(self):
        time_crawl = datetime.datetime.now()
        time_crawl = time_crawl.timestamp()
        return time_crawl

    def extract_post_author(self):
        author = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/div[1]/a/span').text
        return author
    
    def extract_post_title(self):
        return ""

    def extract_post_author_link(self):
        author_link = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/a').get_attribute('href')
        return author_link

    def extract_post_author_avatar(self):
        avatar = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/a/span/img').get_attribute('src')
        return avatar

    def extract_post_created_time(self):
        createTime = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/div[1]/p[2]/span[1]').text
        createTime = format_time(createTime)
        return createTime

    def extract_post_content(self):
        content = self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/div[1]/p[1]').text
        return content

    def extract_post_like(self):
        like = int(self.driver.find_element(
            By.XPATH, f'//*[@id={self.post_id}]/div[1]/p[2]/div/span').text)
        return like

    def extract_post_love(self):
        return 0

    def extract_post_comment(self):
        # comment = self.comment
        return 0

    def extract_post_share(self):
        return 0

    def extract_post_domain(self):
        domain = "www.tiktok.com"
        return domain

    def extract_post_hagtag(self):
        return ""

    def extract_post_music(self):
        return ""

    def extract_post_duration(self):
        return 0

    def extract_post_view(self):
        return 0

    def extract_post_type(self):
        type = "tiktok comment"
        return type

    def extract_post_source_id(self):
        getIDvid = self.driver.find_element(
            By.XPATH, '//*[@class="tiktok-web-player no-controls"]')
        source_id = "tt_" + ((getIDvid.get_attribute('id')).split('-'))[2]
        return source_id