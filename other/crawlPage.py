### LIBRARY  ###
from selenium  import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import json
import pickle
from login import TiktokLogin
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from puzzle import Puzzle



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
driver = webdriver.Chrome(options=options)


### CLASS ###
class TiktokCrawl:
    def __init__(self, driver, type = None, key = None):
        self.driver = driver
        self.type = type
        self.key = key
        self.puzzle = Puzzle(self.driver)
        
    def SearchBox(self):
        search_box = self.driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input')
        search_box.send_keys(self.key)
        button = self.driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/button')
        button.click()
        
    def GetLinkVideo(self):
        
        try:
            time.sleep(5)
            # url = f"https://www.tiktok.com/search/{self.type}?q={self.key}"
            # self.driver.get('https://www.google.com/')
            # time.sleep(8)
            # self.driver.get(url)
            # self.SearchBox()
            # time.sleep(10)
            vidList=[]
            while(len(vidList) < 10):
                vidList=[]
                vid_elem = driver.find_elements(By.XPATH, '//*[@data-e2e="user-post-item-desc"]')
                for vid in vid_elem:
                    vid = vid.find_element(By.TAG_NAME, 'a')
                    vidList.append((vid.get_attribute('href')))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            vidList = vidList[:10]
            return vidList
        except:
            try:
                self.driver.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div')
                self.puzzle.puzzleSolver()
                return self.GetLinkVideo()
            except:
                driver.quit()
    
    def GetPage(self, link):
        account = {}
        self.driver.get(link)
        account['userID'] = driver.find_element(By.XPATH, '//*[@data-e2e="user-title"]').text
        account['userName'] = driver.find_element(By.XPATH, '//*[@data-e2e="user-subtitle"]').text 
        account['following-count'] = driver.find_element(By.XPATH, '//*[@data-e2e="following-count"]').text
        account['followers-count'] = driver.find_element(By.XPATH, '//*[@data-e2e="followers-count"]').text
        account['likes-count'] = driver.find_element(By.XPATH, '//*[@data-e2e="likes-count"]').text
        account['user-bio'] = driver.find_element(By.XPATH, '//*[@data-e2e="user-bio"]').text
        data = self.CrawlVideoAccount()
        account["video"] = data
        with open('accountCrawl.json', 'w') as f:
            json.dump(account, f, indent=4)
        
        
    def CrawlVideoAccount(self):
        vidList = self.GetLinkVideo()
        data = {}
        ### Check video cralwed ###
        for vid in vidList:
            data[vid] = self.CrawlVideo(vid)
        return data
    
    def CrawlListVideo(self):
        vidList = self.GetLinkVideo()
        ### Check video cralwed ###
        for vid in vidList:
            with open('avengers.json', 'r') as f:
                data = json.load(f)
            if vid in data:
                print("This video is crawled")
                continue
            else:
                data[vid] = self.CrawlVideo(vid)
                print(data)
                with open('avengers.json', 'w') as f:
                    json.dump(data, f, indent=4)
        return data
    
    def CrawlVideo(self,vid):
        # wait = WebDriverWait(driver, 10)
        video = {}
        try:
            self.driver.get(vid)
            time.sleep(4)
            try:
                button = driver.find_element(By.XPATH, '//*[@id="login-modal"]/div[2]')
                button.click()
            except:
                pass
                # time.sleep(3)
            time.sleep(3.5)
                # video['Link'] = vid
                
                ### Get Inf Author ###
            getIDvid = self.driver.find_element(By.XPATH, '//*[@class="tiktok-web-player no-controls"]')
            IDvid = ((getIDvid.get_attribute('id')).split('-'))[2]
            video['AuthorID'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-user-avatar"]').get_attribute('href')
            video['AuthorName'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browser-nickname"]/span[1]').text
                
                ### Get Create Time ###
                # video['TimeofVid'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browser-nickname"]/span[3]').text
            createTime_text = self.driver.find_element(By.XPATH,'//*[@id="SIGI_STATE"]').get_attribute('text')
            createTime_text = json.loads(createTime_text)
            createTime = createTime_text["ItemModule"][IDvid]["createTime"]
                
            timestamp = int(createTime)  # Example Unix timestamp
            video["CreateTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
                
                
                ### Get Content ###
            hastag = self.driver.find_elements(By.XPATH, '//*[@data-e2e="browse-video-desc"]/a')
            video['Hastag'] = [elem.get_attribute('href') for elem in hastag]
                # content = self.driver.find_elements(By.XPATH, '//*[@data-e2e="browse-video-desc"]/span')
                # video['Content'] = [elem.text for elem in content]
            video['Content'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-video-desc"]').text 
                # pause = self.driver.find_element(By.XPATH, '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[6]/div[2]/div[1]/div[1]/svg')
                # pause.click()
            video['Music'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="browse-music"]/a').get_attribute('href')
            video['Like count'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="like-count"]').text
            video['Love count'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="undefined-count"]').text
            video['Share count'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="share-count"]').text
            video['Comment count'] = self.driver.find_element(By.XPATH, '//*[@data-e2e="comment-count"]').text

            print(video)
            cmt = CrawlComment(self.driver, count= 100)
            comment = cmt.crawlCmt()
            video['Comment'] = comment
            return video
        except Exception as e:
            print(e)
        
            
class CrawlComment(): 
    def __init__(self, driver, count):
        self.driver = driver
        self.count = count
                    
            
    def scroll(self):
        actions = ActionChains(self.driver)
        cmts=[]
        check = 1
        while((len(cmts) < 50) & (len(cmts) != check) ):
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
        # IDReply = IDRepdiv.get_attribute('id')
        # allCmt[IDh] = thisCmt
        # print(IDh)
        reply = IDRepdiv.find_elements(By.TAG_NAME, 'div')
        thisReply['authorID'] = ((reply[0]).find_element(By.TAG_NAME, 'a')).get_attribute('href')
        infReply = (reply[0].text).split('\n')
        thisReply['authorName'] = infReply[0]
        thisReply['timeReply'] = (infReply[2])[:-5]
        thisReply['contentReply'] = infReply[1]
        thisReply['Like'] = reply[1].text
        return thisReply
    
    def CMT(self, cmt, l):
        # l += 1
        thisCmt={}
        CMTdiv = cmt.find_elements(By.TAG_NAME, 'div')
        IDcmt = CMTdiv[0].get_attribute('id')
        print("CMTdiv: ", len(CMTdiv))

        # print(IDList)
        # Get Inf of CMT
        
        comment = CMTdiv[0].find_elements(By.TAG_NAME, 'div')
        thisCmt['Author ID'] = ((comment[0]).find_element(By.TAG_NAME, 'a')).get_attribute('href')
        infCmt = (comment[0].text).split('\n')
        thisCmt['Author Name'] = infCmt[0]
        thisCmt['Time CMT'] = cmt.driver.find_element(By.XPATH, '//*[@data-e2e="comment-time-1"]').text
        thisCmt['ContentCMT'] = infCmt[1]
        thisCmt['Like'] = comment[1].text
        print(f"Done Crawl CMT {l}")
        # try:
        #     repDiv = cmt.find_element(By.CLASS_NAME, "tiktok-zn6r1p-DivReplyContainer eo72wou1")
        if len(CMTdiv) <= 7:
            thisCmt['Reply'] = 0
        else:
            self.clickViewmore(cmt)
            CMTdiv = cmt.find_elements(By.TAG_NAME, 'div')
            IDList = []
            for div in CMTdiv:
                try:
                    id = div.get_attribute('id')
                except:
                    continue
                IDList.append(id)
            
            IDList = [x for x in IDList if x != '']
            if IDcmt in IDList:
                IDList.remove(IDcmt)
            try: 
                print('Try Find Rep')
                thisCmt["Reply Count"] = len(IDList)
                # print("Reply: ",len(IDList))
                allReply = {}
                for i in range (len(IDList)):
                    thisReply = self.ReplyCmt(IDList[i])
                    allReply[IDList[i]] = thisReply
                thisCmt['Reply']= allReply
            except Exception as e:
                pass
                # print("No find Reply div7")
            
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
                        print("No Rep2")
                        BOOL = False
                        # Tìm các thẻ div của Reply
            except Exception as e:
                print("No Rep 1")
                
    
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
                driver.quit()
    
    
        
        

def main():
    captcha = Puzzle(driver)
    driver.get("https://www.tiktok.com")
    time.sleep(5)
    try:
        button = driver.find_element(By.XPATH, '//*[@id="login-modal"]/div[2]')
        button.click()
    except:
        print("No login div")
    time.sleep(5)
    try:
        print("Check Captcha")
        driver.find_element(By.XPATH, '//*[@id="captcha-verify-image"]')
        # driver.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[1]/div[2]/div')
        captcha.puzzleSolver()
        driver.get("https://www.tiktok.com")
        time.sleep(5)
        try:
                button = driver.find_element(By.XPATH, '//*[@id="login-modal"]/div[2]')
                button.click()
        except:
                print("No login div")
        time.sleep(5)
    except:
        print("No captcha")
    
    print("CRAWLING ........")
    crawl = TiktokCrawl(driver, type = 'video', key = 'avengers')
    crawl.GetPage("https://www.tiktok.com/@_thanhthuy.hhvn_")
    print("DONE CRAWLING >>>")
    driver.quit()
             


### EXECUTE ###
if __name__ == '__main__':
    main()

