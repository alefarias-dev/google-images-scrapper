# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import
from bs4 import BeautifulSoup
import time

image_search = "https://www.google.com.br/search?q=banana&prmd=inv&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj3mdzbnrXZAhWQuFMKHY7DAbYQ_AUIESgB#imgrc=_"

def downloadPage(url):
    path_webdriver = "C:\\webdrivers\\chromedriver.exe"
    driver = webdriver.Chrome(path_webdriver)
    driver.get(url)
    driver.execute_script('window.scrollTo(0, 2000);')
    time.sleep(5)
    html = driver.page_source
    f = open('image.html', 'w', encoding='utf-8')
    f.write(html)
    f.close()

downloadPage(image_search)
