from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *

import _thread
import time
import random
import json
import sys, os, re
import threading

printLock = threading.Lock()
            
def scrapePosts(i):
    try:
        with printLock:
            print(i, ' Starting thread')

        proxies = open('proxies.txt', 'r').read().split('\n')
        
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxies[int(i)],
            'ftpProxy': proxies[int(i)],
            'sslProxy': proxies[int(i)],
            'noProxy': '' # set this value as desired
            })
        
        driver = webdriver.Firefox(executable_path='/home/kazi/Documents/geckodriver')
        # driver = webdriver.Chrome(executable_path='/home/kazi/Documents/chromedriver')
        
        driver.get("https://whatsmyip.org")
        div = driver.find_element_by_id('ip')
        ip = div.text
        with printLock:
            print(i, 'IP', ip)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        with printLock:
            print(exc_type, fname, exc_tb.tb_lineno, e)
        pass
# scrapePosts(0)

for i in range(5):
    try:
        t = threading.Thread(target=scrapePosts, args=(i,))
        t.start()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        with printLock:
            print(exc_type, fname, exc_tb.tb_lineno)
            print(i, 'Exception starting thread: ', e)
        pass