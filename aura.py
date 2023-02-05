import os
import sys

from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import getpass
import random
import time
import datetime as dt

from termcolor import colored
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,ElementNotInteractableException,StaleElementReferenceException,NoSuchElementException
from termcolor import colored
import getpass
class Aura:
    def __init__(self,start_page,end_page):
        self.start_page=start_page
        self.end_page=end_page

        self.link_url = "https://app.goaura.com/a/BJ1W1RoOo/listings"
       

        opts = uc.ChromeOptions()
        opts.add_argument("--lang=en_US")
        # opts.headless = True
        # opts.add_argument('--headless')
        profile=f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data"
       
        self.driver = uc.Chrome(options=opts,user_data_dir=profile, use_subprocess=True)
        self.driver.get(self.link_url)
        
        self.automate()

    def calcProcessTime(self,starttime, cur_iter, max_iter):

        telapsed = time.time() - starttime
        testimated = (telapsed/cur_iter)*(max_iter)

        finishtime = starttime + testimated
        finishtime = f'eta {dt.datetime.fromtimestamp(finishtime).strftime("%H:%M:%S")}'  # in time

        lefttime = testimated-telapsed  # in seconds

        time_left=f"remaining/time {dt.timedelta(seconds=lefttime)}"

        return (time_left, finishtime)


    def automate(self):
        next_page_num=1

        # click on profit
     
        # profit_elm=WebDriverWait(self.driver, 5).until(
        #             EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div/section/section/div[2]/div/section/main/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div/div/table/thead/tr/th[16]/span/div")))
        # self.driver.execute_script("arguments[0].scrollIntoView();", profit_elm)

        # profit_elm.click()
        time.sleep(20)
        started=time.time()
        
        for e in range(1,self.end_page+1):
            
            try:
                
                min_price_input=WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,"input[placeholder='Min Price']")))
                for k,price in enumerate(min_price_input):
                    print(f"[ ] Editing page {next_page_num} price progress {k/len(min_price_input)*100} %")
                    self.driver.execute_script("arguments[0].scrollIntoView();", price)
                  
                    time.sleep(1)

                    for p in range(100):
                        price.send_keys(Keys.BACKSPACE)
                    time.sleep(1)

                    price.send_keys(Keys.RETURN)

                    print(colored(f"Successfully updated price tag {self.calcProcessTime(started,e,self.end_page+1)}","green"))

                    time.sleep(2)
            
            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                        StaleElementReferenceException, NoSuchElementException) as e:
                print("no editable price found")

            elem_tag=f"li[title='{next_page_num}']"
            next_page=WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,elem_tag)))
            
            next_page.click()
            next_page_num+=1
            print(f"Getting page {next_page_num}")

            
            
           
            time.sleep(2)
                
    
if __name__=="__main__":

    Aura(1,100)
