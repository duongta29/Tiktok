### LIBRARY  ###
from selenium  import webdriver
from time import sleep
import time
import pyotp
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import csv
import json
import pickle
from login import TiktokLogin


from selenium.webdriver.chrome.options import Options


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



#### GLOBAL INIT #####
url = 'https://www.tiktok.com/'
account = 'account.json'

### CLASS ###
class TiktokCrawl:
    def __init__(self, driver, type = None, key = None):
        self.driver = driver
        self.type = type
        self.key = key
        
    def SearchBox(self):
        search_box = self.driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input')
        search_box.send_keys(self.key)
        button = self.driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/button')
        button.click()
        
        
    def GetVideo(self):
        time.sleep(5)
        # url = f"https://www.tiktok.com/search/{self.type}?q={self.key}"
        # self.driver.get('https://www.google.com/')
        # time.sleep(8)
        # self.driver.get(url)
        self.SearchBox()
        time.sleep(10)
        try:
            video = self.driver.find_element(By.XPATH, '//*[@class="tiktok-c83ctf-DivWrapper e1cg0wnj1"]')
            video.click()
        except:
            time.sleep(10)
            video = self.driver.find_element(By.XPATH, '//*[@class="tiktok-c83ctf-DivWrapper e1cg0wnj1"]')
            video.click()
        time.sleep(5)
        getIDvid = self.driver.find_element(By.XPATH, '//*[@class="tiktok-web-player no-controls"]')
        IDvid = ((getIDvid.get_attribute('id')).split('-'))[2]
        # print(ID)
        with open('dataCrawled.json', 'r') as f:
            data = json.load(f)
        if IDvid in data:
            print("This video is crawled")
        else:
            start = time.time()
            data[IDvid] = self.Crawl()
            print(data)
            with open('new.json', 'w') as f:
                json.dump(data, f, indent=4)
            
            
    
        
    def Crawl(self):
        vid = {}
            # Get Author Information #
        author = {}
        elemAu = self.driver.find_element(By.XPATH, '//*[@class="tiktok-85dfh6-DivInfoContainer evv7pft0"]')
        Au = elemAu.text.split('\n')
        author['ID'] = Au[0]
        author['Name'] = Au[1]
        vid['author'] = author
            
            # Get Time of Post #
        vid['time'] = Au[3]
            
            # Get Content #
        elemCon = self.driver.find_element(By.XPATH, '//*[@class="tiktok-1vrp1yb-DivContainer ejg0rhn0"]')
        vid['content'] = elemCon.text
            
            # Get Link Music #
        elemMus = self.driver.find_element(By.XPATH, '//*[@class="epjbyn1 tiktok-v80f7r-StyledLink-StyledLink er1vbsz0"]')
        vid['Music'] = elemMus.get_attribute('href')
            
            # Get Count of Like , Commment, Share #
        elemLike = self.driver.find_elements(By.XPATH, '//*[@class="tiktok-1y8adbq-StrongText e1hk3hf92"]')
        vid['Count of Like'] = (elemLike[0]).text
        vid['Count of Comment'] = (elemLike[1]).text
        vid['Count of Share'] = (elemLike[2]).text
            
            # Crawl Comment # tiktok-15bav38-DivCommentListContainer ekjxngi3
        cmt = CrawlComment(self.driver, count= 100)
        comment = cmt.crawlCmt()
        vid['Comment'] = comment
        return vid
            

        
        
class CrawlComment(): 
    def __init__(self, driver, count):
        self.driver = driver
        self.count = count
        
    def scroll(self):
        actions = ActionChains(self.driver)
        cmts=[]
        while(len(cmts) < 50):
            comments_section = self.driver.find_element(By.XPATH, '//*[@data-e2e="search-comment-container"]/div')
            actions.move_to_element(comments_section)
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", comments_section)
            cmts = self.driver.find_elements(By.XPATH, '//*[@class="tiktok-1i7ohvi-DivCommentItemContainer eo72wou0"]')
            self.cmts = cmts
        time.sleep(3)
        try:
            scrollup = self.driver.find_element(By.XPATH, '//*[@class="tiktok-1yyj082-DivButton e1hknyby1"]')
            scrollup.click()
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
    
    def CMT(self, cmt):
    # cmt : [@class="tiktok-1i7ohvi-DivCommentItemContainer eo72wou0"]
    # có 2 thẻ div, một thẻ chứ ND cmt chính, 1 thẻ chứa ND của các Reply
        thisCmt={}
        CMTdiv = cmt.find_elements(By.TAG_NAME, 'div')
        IDcmt = CMTdiv[0].get_attribute('id')
        print("CMTdiv: ", len(CMTdiv))
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
        print(IDList)
        # Get Inf of CMT
        
        comment = CMTdiv[0].find_elements(By.TAG_NAME, 'div')
        thisCmt['Author ID'] = ((comment[0]).find_element(By.TAG_NAME, 'a')).get_attribute('href')
        infCmt = (comment[0].text).split('\n')
        thisCmt['Author Name'] = infCmt[0]
        thisCmt['Time CMT'] = (infCmt[2])[:-5]
        thisCmt['ContentCMT'] = infCmt[1]
        thisCmt['Like'] = comment[1].text
        print("Done Crawl CMT")
        # try:
        #     repDiv = cmt.find_element(By.CLASS_NAME, "tiktok-zn6r1p-DivReplyContainer eo72wou1")
        if len(CMTdiv) <= 7:
            thisCmt['Reply'] = 0
        else:
            self.clickViewmore(cmt)
            try: 
                print('Try Find Rep')
                print("Reply: ",len(IDList))
                allReply = {}
                for i in range (len(IDList)):
                    thisReply = self.ReplyCmt(IDList[i])
                    allReply[IDList[i]] = thisReply
                thisCmt['Reply']= allReply
            except Exception as e:
                print("No find Reply div7")
            
        return IDcmt, thisCmt
    
    def clickViewmore(self,cmt):
        BOOL = True
        for i in range(3):
            try:
                rep1 = cmt.find_element(By.XPATH, '//*[@data-e2e="view-more-1"]')
                rep1.click()
                time.sleep(2)
                while(BOOL):
                    try:
                        rep2 = cmt.find_element(By.XPATH, '//*[@data-e2e="view-more-2"]')
                        rep2.click()
                        time.sleep(2)
                    except Exception as e:
                        print("No Rep2")
                        BOOL = False
                        # Tìm các thẻ div của Reply
            except Exception as e:
                print("No Rep 1")
                
    
    def crawlCmt(self):
        self.scroll()
        allCmt={}
        for cmt in self.cmts:
            IDh, thisCmt = self.CMT(cmt)
            allCmt[IDh] = thisCmt
        return allCmt




        

### DEFINE ###
def getListCrawl(driver):
    driver.find_elements(By.XPATH,'//*[@aria-label=" Watch in full screen"]')
    
def main():
    # driver = webdriver.Chrome(executable_path ='chromedriver.exe',options=options)
    driver.get(url)
    time.sleep(3)
    # ttLogin = TiktokLogin(driver, account)
    # ttLogin.loginTiktokwithCookie()
    crawl = TiktokCrawl(driver, type='video', key = 'avengers')
    start = time.time()
    crawl.GetVideo()
    end = time.time()



### EXECUTE ###
if __name__ == '__main__':
    main()
