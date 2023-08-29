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

from login import TiktokLogin
from selenium.webdriver.chrome.options import Options

import random
from selenium.webdriver.common.keys import Keys
import pickle
import csv




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
puzzle = Puzzle(driver)

### CLASS ###
class TiktokCrawl:
    def __init__(self, driver,i,  type = None, key = None, ):
        self.i = i
        self.driver = driver
        self.type = type
        self.key = key
        
        
    def SearchBox(self):
        search_box = self.driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input')
        search_box.send_keys(self.key)
        button = self.driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/button')
        button.click()
        
    def GetLinkVideo(self) -> list:
        print('GetLink')
        # time.sleep(5)
        url = f"https://www.tiktok.com/search/{self.type}?q={self.key}"
            # self.driver.get('https://www.google.com/')
            # time.sleep(8)
        self.driver.get(url)
            # self.SearchBox()
        time.sleep(3)
        try:
            puzzle.check_captcha()
            return self.CrawlListVideo()
        except:
            count = 1
            vidList=[]
            while(len(vidList) != count):
                count = len(vidList)
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
       
            
                # driver.quit()
                # time.sleep(3)
                # driver = webdriver.Chrome(options=options)
                # return self.CrawlListVideo()
                
    
    def CrawlListVideo(self):
        count = 0
        
        try:
            vidList = self.GetLinkVideo()
            print(vidList)
            ### Check video cralwed ###
            start_all = time.time()
            for vid in vidList:
                try: 
                    with open('dataCrawled.txt', 'r') as f:
                        dataCrawled = f.read()
                    if vid in dataCrawled:
                        print("This video is crawled")
                        continue
                    else:
                        start = time.time()
                        data = {}
                        data[vid] = self.CrawlVideo(vid)
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
                            json.dump(data, f, indent=4)

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
        
    
    def CrawlVideo(self,vid):
        # wait = WebDriverWait(driver, 10)
        video = {}
        try:
            self.driver.get(vid)
            time.sleep(3)
            try:
                button = driver.find_element(By.XPATH, '//*[@id="login-modal"]/div[2]')
                button.click()
            except:
                pass
                # time.sleep(3)
            time.sleep(2)
                # video['Link'] = vid
                
                ### Get Inf Author ###
            getIDvid = self.driver.find_element(By.XPATH, '//*[@class="tiktok-web-player no-controls"]')
            IDvid = ((getIDvid.get_attribute('id')).split('-'))[2]
            video['time_crawl'] = datetime.datetime.now()
            video['author'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browser-nickname"]/span[1]').text
            video['author_link'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-user-avatar"]').get_attribute('href')
            video['avatar'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-user-avatar"]/div/span/img').get_attribute('src')
                
                ### Get Create Time ###
                # video['TimeofVid'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browser-nickname"]/span[3]').text
            infor_text = self.driver.find_element(By.XPATH,'//*[@id="SIGI_STATE"]').get_attribute('text')
            infor_text = json.loads(infor_text)
            createTime = infor_text["ItemModule"][IDvid]["createTime"]
                
            timestamp = int(createTime)  # Example Unix timestamp
            video["created_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            video['like'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="like-count"]').text
            video['love'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="undefined-count"]').text
            video['comment'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="comment-count"]').text
            video['share'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="share-count"]').text
            video['domain'] = 'www.tiktok.com'
            video['id'] = IDvid
                ### Get Content ###
            hastag = self.driver.find_elements(By.XPATH, '//*[@data-e2e="browse-video-desc"]/a')
            video['hastag'] = [elem.text for elem in hastag]
                # content = self.driver.find_elements(By.XPATH, '//*[@data-e2e="browse-video-desc"]/span')
                # video['Content'] = [elem.text for elem in content]
            video['content'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-video-desc"]').text 
                # pause = self.driver.find_element(By.XPATH, '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[6]/div[2]/div[1]/div[1]/svg')
                # pause.click()
            video['music'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-music"]/a').get_attribute('href')
            video['duration'] = infor_text["ItemModule"][IDvid]["video"]["duration"]
            video['view'] = infor_text["ItemModule"][IDvid]["stats"]["playCount"]
            # "diggCount": 65200,
            #     "shareCount": 1475,
            #     "commentCount": 1655,
            #     "playCount": 1700000,
            #     "collectCount": "3398"
            

            # print(video)
            cmt = CrawlComment(self.driver, count= 100)
            comment = cmt.crawlCmt()
            video['Comment'] = comment
            return video
        except Exception as e:
            # print(e)
            pass
        
            
class CrawlComment(): 
    def __init__(self, driver, count):
        self.driver = driver
        self.count = count
            
            
    def scroll(self):
        actions = ActionChains(self.driver)
        cmts=[]
        check = 1
        while((len(cmts) < 1000) & (len(cmts) != check) ):
                # comments_section = self.driver.find_element(By.XPATH, '//*[@data-e2e="search-comment-container"]/div')
                # actions.move_to_element(comments_section)
            check = len(cmts)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            cmts = self.driver.find_elements(By.XPATH, '//*[@class="tiktok-1i7ohvi-DivCommentItemContainer eo72wou0"]')
            self.cmts = cmts
            time.sleep(3)
        try:
            driver.execute_script("window.scrollTo(0, 0);")
        except:
            pass
        time.sleep(3)
        
    

    def ReplyCmt(self, ID):
        thisReply={}
                # print(cmt)
        IDRepdiv = self.driver.find_element(By.ID, ID)
        IDReply = IDRepdiv.get_attribute('id')
        # allCmt[IDh] = thisCmt
        # print(IDh)
        reply = IDRepdiv.find_elements(By.TAG_NAME, 'div')
        thisReply['authorID'] = ((reply[0]).find_element(By.TAG_NAME, 'a')).get_attribute('href')
        # infReply = (reply[0].text).split('\n')
        thisReply['authorName'] = self.driver.find_element(By.XPATH, f'//*[@id={IDReply}]/div[1]/a/span').text
        thisReply['timeReply'] = self.driver.find_element(By.XPATH, f'//*[@id={IDReply}]/div[1]/p[2]/span[1]').text
        thisReply['contentReply'] = self.driver.find_element(By.XPATH, f'//*[@id={IDReply}]/div[1]/p[1]').text
        thisReply['Like'] = reply[1].text
        return thisReply
    
    def CMT(self, cmt, l):
        # l += 1
        thisCmt={}
        CMTdiv = cmt.find_elements(By.TAG_NAME, 'div')
        IDcmt = CMTdiv[0].get_attribute('id')
        # print("CMTdiv: ", len(CMTdiv))

        # print(IDList)
        # Get Inf of CMT
        # //*[@id="7205706238175691526"]
        comment = CMTdiv[0].find_elements(By.TAG_NAME, 'div')
        thisCmt['Author ID'] = ((comment[0]).find_element(By.TAG_NAME, 'a')).get_attribute('href')
        # infCmt = (comment[0].text).split('\n')
        thisCmt['Author Name'] = self.driver.find_element(By.XPATH, f'//*[@id={IDcmt}]/div[1]/a/span').text
        thisCmt['Time CMT'] = self.driver.find_element(By.XPATH, f'//*[@id={IDcmt}]/div[1]/p[2]/span[1]').text
        thisCmt['ContentCMT'] = self.driver.find_element(By.XPATH, f'//*[@id={IDcmt}]/div[1]/p[1]').text
        thisCmt['Like'] = comment[1].text
        # try:
        #     repDiv = cmt.find_element(By.CLASS_NAME, "tiktok-zn6r1p-DivReplyContainer eo72wou1")
        # if len(CMTdiv) <= 7:
        #     thisCmt['Reply'] = 0
        # else:
        #     self.clickViewmore(cmt)
        #     CMTdiv = cmt.find_elements(By.TAG_NAME, 'div')
        #     IDList = []
        #     for div in CMTdiv:
        #         try:
        #             id = div.get_attribute('id')
        #         except:
        #             continue
        #         IDList.append(id)
            
        #     IDList = [x for x in IDList if x != '']
        #     if IDcmt in IDList:
        #         IDList.remove(IDcmt)
        #     try: 
        #         # print('Try Find Rep')
        #         thisCmt["Reply Count"] = len(IDList)
        #         # print("Reply: ",len(IDList))
        #         allReply = {}
        #         for i in range (len(IDList)):
        #             thisReply = self.ReplyCmt(IDList[i])
        #             allReply[IDList[i]] = thisReply
        #         thisCmt['Reply']= allReply
        #     except Exception as e:
        #         pass
        #         # print("No find Reply div7")
        # # print(f"Done Crawl CMT {l}")
        return IDcmt, thisCmt
    
    def clickViewmore(self,cmt):
        BOOL = True
        wait = WebDriverWait(cmt, 5)
        for i in range(3):
            try:
                rep1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-e2e="view-more-1"]')))
                rep1.click()
                time.sleep(2)
                while(BOOL):
                    try:
                        # Chờ tối đa 10 giây cho phần tử "view-more-2" xuất hiện
                        rep2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-e2e="view-more-2"]')))
                        # Nhấp vào phần tử
                        rep2.click()
                    except Exception as e:
                        # print("No Rep2")
                        BOOL = False
                        # Tìm các thẻ div của Reply
            except Exception as e:
                # print(e)
                # print("No Rep 1")
                pass
                
    
    def crawlCmt(self):
        l = 0
        try:
            self.scroll()
            allCmt={}
            for cmt in self.cmts:
                l += 1
                IDh, thisCmt = self.CMT(cmt,l)
                allCmt[IDh] = thisCmt
            return allCmt
        except:
            try:
                self.driver.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div')
                self.puzzle.puzzleSolver()
                return self.GetLinkVideo()
            except:
                pass
    
    
        
        

def main():
    captcha = Puzzle(driver)
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
    time_crawl = time.time()
    i = 0
    key_list = ['marvel avenger', 'iron man','captain America', 'natasha romanoff','hulk','Thor Odinson','bat man','superman', 'the flash']
    for key_word in key_list:
        crawl = TiktokCrawl(driver, i ,type = 'video', key = key_word )
        i += crawl.CrawlListVideo()
    print("DONE CRAWLING >>>")
    driver.quit()
    time_crawled = time.time()
    print("Total Time: ", time_crawled-time_crawl)


### EXECUTE ###
if __name__ == '__main__':
    main()

