### LIBRARY  ###
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium  import webdriver
from typing import Callable, List, Optional, Tuple
from selenium.webdriver.common.by import By
import time
from puzzle import Puzzle
from post_model import Post
from utils.common_utils import CommonUtils
from post_tiktok_etractor import PostTikTokExtractor, PostCommentExtractor
import re
from unidecode import unidecode
# from login import TiktokLogin


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
# driver = webdriver.Chrome(options=options)


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
    # driver = webdriver.Chrome(options=options)
    
    def __init__(self, driver : WebDriver, keyword: str, keyword_noparse: List, callback: Optional[Callable[[Post], None]] = None):
        self.url = f"{self.TIKTOK_SEARCH_LINK}{keyword}"
        self.callback = callback
        self.driver =  driver
        self.driver.get(url = self.url)
        # self.driver.implicitly_wait(1000)
        self.keyword_noparse = keyword_noparse
        self.keyword = keyword

    def preprocess(self,text):
        return re.findall(r'\w+', text.lower())
    
    def unsigned_text(self, content : str):
        return unidecode(content).lower()
        
    def get_links_post(self) -> list:
        print('---> GET LINK LIST <---')
        # self.driver.get(self.url)
        try:
            time.sleep(3)
            self.driver.find_element(By.Xpath, '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div')
            puzzle.puzzleSolver()
            return self.get_links_post()
        except:
            count = 1
            vidList=[]
            vid_list_elem =[]
            while(len(vid_list_elem) != count):
                # data-e2e="search-common-link"
                count = len(vid_list_elem)
                vidList=[]
                vid_list_elem = self.driver.find_elements(By.XPATH, '//*[@class="tiktok-1soki6-DivItemContainerForSearch e19c29qe11"]')
                print("len vid: ", len(vid_list_elem))
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            for vid in vid_list_elem:
                    # print("###################################################")
                    link = vid.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    hagtag = []
                    elem = vid.find_elements(By.TAG_NAME, 'a')
                    # link = elem.get_attribute('href')
                    for e in elem:
                        try:
                            n = e.get_attribute('text').replace("#", "")
                            hagtag.append(n.replace(" ", ""))
                        except:
                            pass
                    thehagtag = hagtag[1:-1]
                    thecontent = vid.find_element(By.TAG_NAME, 'span').text
                    def filter_post(key, content, hagtag):
                        result = set()
                        content_prep = self.preprocess(self.unsigned_text(content))
                        key_prep = self.preprocess(self.unsigned_text(key))
                        key_uns =[]
                        for key_word in key_prep:
                            key_word = self.unsigned_text(key_word)
                            key_uns.append(key_word.replace(" ", ""))
                            if (key_word in content_prep):
                                result.update(key_word)
                            else:
                                continue
                            key_uns.append(key_word.replace(" ", ""))
                        
                        key_uns.append((self.unsigned_text(key)).replace(" ", ""))
                        # print("key_uns: ",key_uns)
                        for a in key_uns:
                            if a in hagtag:
                                result.update(a)
                        return result
                    check = filter_post(self.keyword, thecontent,thehagtag)

                    # check = filter_post(self.keyword, content)
                    if check: 
                        vidList.append(link)
                    else:
                        print(f"Filter out link {link}")
                        continue 
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
                        print(f"Start crawl link : {vid}")
                        start = time.time()
                        # data = {}
                        self.driver.get(vid)
                        post_extractor: PostTikTokExtractor = PostTikTokExtractor(driver=self.driver, link = vid)
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
                        
                        # print(data)
                        with open('dataCrawled.txt', 'a') as f:
                            f.write(vid)
                            f.write("\n")
                        
                        with open("result.txt", "a", encoding="utf-8") as file:
                            file.write(f"{str(post)}\n")
                            if post.is_valid:
                                file.write(f"🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷🇧🇷\n")
                            else:
                                file.write(f"🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈\n")
                        end = time.time()
                        print(f"Time for video {count}: ",end - start)
                except Exception as e:
                    print(e)
                    # print("count: ", count)
                    pass
                try: 
                    self.crawl_comment(vid)
                except Exception as e:
                    print(e)
                # if count == len(vidList):
                #     break
            end_all = time.time()
            print(f"Time for {count} video: ", end_all - start_all)
        except:
            pass
        # return self.i
    
    def extract_numbers_from_string(self, string):
        pattern = r'\d+'
        numbers = re.findall(pattern, string)
        return numbers
    
    def crawl_comment(self, link):
        def scroll():
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
            list_cmt = scroll()
            for cmt in list_cmt:
                comment_id = cmt.find_element(By.TAG_NAME, 'div').get_attribute('id')
                
                try: 
                        button = (cmt.find_element(By.XPATH, '//*[@data-e2e="comment-hide"]'))
                        button.click()
                except:
                        pass
                try:
                        div = cmt.find_element(By.TAG_NAME, 'p')
                        count_reply = div.text
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
            
        
        
            

def main():
    # driver.quit()
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tiktok.com")
    post_crawl = PostSearchExtractor(driver = driver, keyword="captain america", keyword_noparse=[])
    post_crawl.post_extract()
    
    
### EXECUTE ###
if __name__ == '__main__':
    main()