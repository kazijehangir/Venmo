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

def getPostInLink(link, driver):
    posts = []
    for i in range(4, 10):
        try:
            e = driver.find_element_by_id("u_0_" + str(i))
            text = str(e.text)
            # with printLock:
            #     print("Found post...")
            post = {}
            post['author'] = text.split('\n')[0]
            post['date'] = text.split('\n')[-2].split('·')[0]
            post['text'] = '\n'.join(text.split('\n')[1:-2])
            with printLock:
                print(post)
            posts.append(post)
        except Exception as e:
            with printLock:
                print('Exception', e)
            continue
    outbound = driver.find_elements_by_class_name('i')
    links = [div.find_element_by_css_selector('a').get_attribute('href') for div in outbound[1:]]
    texts = [div.find_element_by_css_selector('a').text for div in outbound[1:]]
    for i in range(len(links)):
        if texts[i] == 'Show more':
            with printLock:
                print('Found show more link:', links[i])
                print('With text:', texts[i])
            time.sleep(random.uniform(5, 30))
            driver.get(links[i])
            posts.extend(getPostInLink(links[i], driver))
            break
    return posts

def getPostInProfile(link, driver):
    posts = []
    try:
        time.sleep(random.uniform(5, 30))
        driver.get(link)
        time.sleep(random.uniform(5, 30))
        driver.get(driver.current_url + '&v=timeline')
        outbound = driver.find_elements_by_class_name('i')
        links = [div.find_element_by_css_selector('a').get_attribute('href') for div in outbound[1:]]
        texts = [div.find_element_by_css_selector('a').text for div in outbound[1:]]
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        with printLock:
            print(exc_type, fname, exc_tb.tb_lineno, e)
        pass
    try:
        posts = getPostInLink(link, driver)
        for i in range(len(links)):
            if re.match(r'[0-9]{4}', texts[i]):
                with printLock:
                    print('Found outbound year link:', links[i])
                    print('With text:', texts[i])
                time.sleep(random.uniform(5, 30))
                driver.get(links[i])
                posts.extend(getPostInLink(links[i], driver))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        with printLock:
            print(exc_type, fname, exc_tb.tb_lineno, e)
        pass
    return posts
            
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
        driver.get("https://www.facebook.com/")
        with printLock:
            print(i, 'Started driver')

        time.sleep(random.uniform(5, 30))

        logins = open('fakeprofiles.txt', 'r').read().split('\n')
        login = logins[int(i)]
        email = login.split(',')[0]
        passw = login.split(',')[1]

        inputEmail = driver.find_element_by_id("email")
        inputEmail.send_keys(email)
        inputPass = driver.find_element_by_id("pass")
        inputPass.send_keys(passw)

        time.sleep(random.uniform(5, 30))

        inputPass.submit()
        with printLock:
            print(i , 'Logged in successfully with', email, passw)
        profiles = open('profiles_' + str(i) + '.txt', 'r').read().split('\n')
        outfile = open('posts_' + str(i) + '.json', 'a')
        done = open('done_' + str(i) + '.txt', 'a')
        for j, prof in enumerate(profiles):
            time.sleep(random.uniform(5, 30))
            link = "https://mbasic.facebook.com/" + prof.strip()
            with printLock:
                print(i, 'Scraping profile: ', link)
            posts = getPostInProfile(link, driver)
            json.dump({prof: posts} , outfile)
            outfile.write('\n')
            done.write(prof)
            done.write('\n')
            if not (j % 5):
                outfile.flush()
                done.flush()
                os.fsync(outfile)
                os.fsync(done)
            with printLock:
                print(i, 'Got ' + str(len(posts)) + ' posts for profile ' + prof)
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