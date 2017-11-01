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


def getProxyList():
    proxies = []
    driver = webdriver.Firefox(
        executable_path='/home/jehangir/Documents/geckodriver')
    driver.get('https://free-proxy-list.net/')
    odd = driver.find_elements_by_class_name('odd')
    for row in odd:
        proxy = row.find_elements_by_tag_name('td')
        ip = proxy[0].text
        port = proxy[1].text
        # print('cell', cell)
        print('Found proxy:', ip, port)
        proxies.append(ip + ':' + port)
    even = driver.find_elements_by_class_name('even')
    for row in even:
        proxy = row.find_elements_by_tag_name('td')
        ip = proxy[0].text
        port = proxy[1].text
        # print('cell', cell)
        print('Found proxy:', ip, port)
        proxies.append(ip + ':' + port)

    driver.close()
    print("Got", len(proxies), "proxies.")
    return proxies

proxies = getProxyList()


def scrapePosts(i):
    try:
        with printLock:
            print(i, ' Starting thread')

        proxy = proxies[int(i)].split(':')[0]
        port = int(proxies[int(i)].split(':')[1])
        print('Creating driver with proxy,port', proxy, port)

        fp = webdriver.FirefoxProfile()
        fp.set_preference('network.proxy.ssl_port', int(port))
        fp.set_preference('network.proxy.ssl', proxy)
        fp.set_preference('network.proxy.http_port', int(port))
        fp.set_preference('network.proxy.http', proxy)
        fp.set_preference('network.proxy.type', 1)
        # proxy = Proxy({
        #     'proxyType': ProxyType.MANUAL,
        #     'httpProxy': proxies[int(i)],
        #     'ftpProxy': proxies[int(i)],
        #     'sslProxy': proxies[int(i)],
        #     'noProxy': ''  # set this value as desired
        #     })

        driver = webdriver.Firefox(
            executable_path='/home/jehangir/Documents/geckodriver',
            firefox_profile=fp)
        # driver = webdriver.Chrome(
        # executable_path='/home/jehangir/Documents/chromedriver')

        driver.get("https://whatsmyip.org")
        div = driver.find_element_by_id('ip')
        ip = div.text
        with printLock:
            print(i, 'IP', ip)
        driver.close()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        with printLock:
            print(exc_type, fname, exc_tb.tb_lineno, e)
        pass
# scrapePosts(0)

NUM_THREADS = 5
if len(proxies) < NUM_THREADS:
    print("Not enough proxies found.")

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