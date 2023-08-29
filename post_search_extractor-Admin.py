from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Callable, List, Optional, Tuple
from selenium.webdriver.common.by import By
import time
from post_filter import check
from puzzle import Puzzle
from post_model import Post
from utils.common_utils import CommonUtils
from post_tiktok_etractor import PostTikTokExtractor
import json
import re

puzzle = Puzzle


class PostElementIterator:
    def __init__(self, post_element_list: List[WebElement]):
        self.post_element_list = post_element_list
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.post_element_list):
            raise StopIteration

        post = self.post_element_list[self.index]
        self.index += 1
        return post

    def update(self, post_element_list: List[WebElement]):
        self.post_element_list = post_element_list
        

class PostSearchExtractor:
    driver: WebDriver
    TIKTOK_SEARCH_LINK: str = "https://www.tiktok.com/search/video?q="
    posts: List[Post] = []
    callback: Optional[Callable[[Post], None]] = None
    
    def __init__(self, driver: WebDriver, keyword: str, keyword_noparse: List, callback: Optional[Callable[[Post], None]] = None):
        self.url = f"{self.TIKTOK_SEARCH_LINK}{keyword}"
        self.callback = callback
        self.driver = driver
        self.driver.get(self.url)
        self.driver.implicitly_wait(1000)
        self.keyword_noparse = keyword_noparse
        self.keyword = keyword

    def preprocess(text):
        return re.findall(r'\w+', text.lower())
        
    def get_links_post(self) -> list:
        print('---> GET LINK LIST <---')
        # self.driver.get(self.url)
        try:
            self.driver.find_element(By.Xpath, '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div')
            puzzle.puzzleSolver()
            return self.get_links_post()
        except:
            count = 1
            vidList=[]
            while(len(vidList) != count):
                count = len(vidList)
                vidList=[]
                vid_elem = self.driver.find_elements(By.XPATH, '//*[@class="tiktok-1soki6-DivItemContainerForSearch e19c29qe11"]')
                for vid in vid_elem:
                    vid_link = vid.find_element(By.XPATH, '//*[@data-e2e="search_video-item"]/div/div/a')
                    ### Check to right video for key
                    content = vid.find_element(By.XPATH, '//*[@data-e2e="search-card-video-caption"]').text
                    def filter_post(key, content):
                        result = set()
                        content = self.preprocess(content)
                        for key_word in self.preprocess(key):
                            if key_word in content:
                                result.update(key_word)
                            else:
                                continue
                        return result

                    check = filter_post(self.keyword, content)
                    if check: 
                        vidList.append((vid_link.get_attribute('href')))
                    else:
                        print(f"Filter out link {(vid_link.get_attribute('href'))}")
                print("len vid: ", len(vidList))
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            vidList = vidList
            return vidList
        

    def post_extract(self):
        count = 0
        try:
            vidList = self.get_links_post()
            # print(vidList)
            ### Check video cralwed ###
            start_all = time.time()
            for vid in vidList:
                try: 
                    with open('dataCrawled.txt', 'r') as f:
                        data_crawled = f.read()
                    if vid in data_crawled:
                        print("This video is crawled")
                        continue
                    else:
                        start = time.time()
                        # data = {}
                        post_extractor: PostTikTokExtractor = PostTikTokExtractor(driver=self.driver)
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
                        self.i += 1
                        # print(data)
                        with open('dataCrawled.txt', 'a') as f:
                            f.write(vid)
                            f.write("\n")
                        folder_path = 'dataCrawled'
                        file_name = f'link{self.i}'

                        # Tạo đường dẫn đến tệp tin JSON
                        file_path = f"{folder_path}/{file_name}.json"
                        with open(file_path, 'w') as f:
                            json.dump(post, f, indent=4)

                        end = time.time()
                        print(f"Time for video {count}: ",end - start)
                except:
                    print("count: ", count)
                    pass
                if count == len(vidList):
                    break
            end_all = time.time()
            print(f"Time for {count} video: ", end_all - start_all)
        except:
            pass
        return self.i
    

def main():
    pass
    
    
    
