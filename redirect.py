from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import _thread
import time
import random
import json
import sys, os
import threading

# driver = webdriver.Firefox(executable_path='/home/jehangir/Documents/geckodriver')
driver = webdriver.Chrome(executable_path='/home/jehangir/Documents/chromedriver')
driver.get("https://www.facebook.com/")
print('Started driver')
time.sleep(random.uniform(1, 3))

inputEmail = driver.find_element_by_id("email")
inputEmail.send_keys("jehangir.kazi@hotmail.com")
inputPass = driver.find_element_by_id("pass")
# inputEmail.send_keys(Keys.TAB)
# inputPass = driver.switch_to.active_element['value']

inputPass.send_keys("Ultramantizz11")
time.sleep(random.uniform(1, 3))

inputPass.submit()
print('Logged in successfully...')
time.sleep(random.uniform(1, 3))

driver.get('https://mbasic.facebook.com/1219056607')