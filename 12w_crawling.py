#%%
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By


id = 'selenium.11_'
pw = 'selenium11'

chromedriver = r'./chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(10)

driver.get('https://www.instagram.com/?hl=ko')

time.sleep(3)

id_inp = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label')
id_inp.click()
id_inp.send_keys(id)

pw_inp = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label')
pw_inp.click()
pw_inp.send_keys(pw)

log_btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
log_btn.click()

time.sleep(1)
option_btn = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
option_btn.send_keys(Keys.ENTER)

AlarmPopup = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]')
AlarmPopup.send_keys(Keys.ENTER)
time.sleep(2)


serch = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input')
serch.send_keys('#부산대양산캠퍼스')
time.sleep(3)
serch.send_keys(Keys.ENTER)
serch.send_keys(Keys.ENTER)

driver.find_element_by_css_selector('div._aagw').click()
time.sleep(5)

results = []
count = 100
for i in range(count):
    data = driver.find_elements_by_css_selector("a.oajrlxb2._aa9_._a6hd")
    for j in range(len(data)):
        results.append(data[j].text.replace("#","")) 
    
    if (i+1)%10 == 0: 
        print('{}번째 게시물 완료'.format(i+1))
    driver.find_element_by_css_selector('div._aaqg._aaqh > button').click()
print(results)
driver.quit()

data = pd.DataFrame(results)
data.to_csv('./data.csv')

import nltk
import matplotlib.pyplot as plt
results_str = " ".join(results) 
tokens = results_str.split(" ") 
text = nltk.Text(tokens) 
topWord = text.vocab().most_common(30) 
count = 30
xlist = [a[0] for a in topWord[:count ]]
ylist = [a[1] for a in topWord[:count ]]

from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
    
plt.figure(figsize = (10,5)) 
plt.xlabel('단어')
plt.xticks(rotation=70) 
plt.ylabel('Count') 
plt.title('키워드 상위 '+str(count)+' 단어')
plt.ylim([0, 150]) 
plt.bar(xlist,ylist)


from ast import keyword
import os
import urllib.request
import datetime
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")


def doScrollDown(whileSeconds, driver):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break

header_n = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

def crawl(keywords):
    path = "https://www.google.com/search?q=" + keywords + "&newwindow=1&rlz=1C1CAFC_enKR908KR909&sxsrf=ALeKk01k_BlEDFe_0Pv51JmAEBgk0mT4SA:1600412339309&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj07OnHkPLrAhUiyosBHZvSBIUQ_AUoAXoECA4QAw&biw=1536&bih=754"
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(3)
    driver.get(path)
    driver.maximize_window()
    time.sleep(1)

    counter = 0
    succounter = 0

    print(os.path)
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/' + keywords):
        os.mkdir('data/' + keywords)

    for x in driver.find_elements_by_class_name('rg_i.Q4LuWd'):
        counter = counter + 1
        print(counter)
        
        img = x.get_attribute("data-src")
        if img is None:
            img = x.get_attribute("src")
        print(img)

        imgtype = 'jpg'

        try:
            raw_img = urllib.request.urlopen(img).read()
            File = open(os.path.join('data/' + keywords, keywords + "_" + str(counter) + "." + imgtype), "wb")
            File.write(raw_img)
            File.close()
            succounter = succounter + 1
        except:
            print('error')

    print(succounter, "succesfully downloaded")
    driver.close()

crawl('부산대양산캠퍼스')

