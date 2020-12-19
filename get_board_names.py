from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import sys
from models import Ptt_board_names 
from main import db 

def main():
    '''
        get ptt board names from https://www.ptt.cc/bbs/hotboards.html 
    '''
    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument('--headless')
#    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())
    
    driver.get('https://www.ptt.cc/bbs/hotboards.html')
    
    items = driver.find_elements_by_class_name('b-ent')

    board_name_list = []
    ### web crawler
    for i in range(len(items)):
        xpath = '//*[@id="main-container"]/div[2]/div[' + str(i+1) + ']/a/div[1]'
        board_name = driver.find_element_by_xpath(xpath).get_attribute('innerHTML')
        board_name_list.append(board_name)
    print(board_name_list)

    ### put into db  
    for i in range(len(board_name_list)):
        board = Ptt_board_names()
        board.board_name = board_name_list[i]
        db.session.add(board)
        db.session.commit()
    

if __name__ == '__main__':
    main()
