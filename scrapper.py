# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, os

def download_images(class_name, image_src_list):
    os.mkdir(class_name)
    images_downloaded = 0
    for index, image_src in enumerate(image_src_list):
        try:
            urlretrieve(image_src, class_name+"/"+class_name+str(index)+'.jpg')
            print('download [OK]:', image_src)
            images_downloaded += 1
        except:
            print('download [FAILED]:', image_src)
    print(images_downloaded, 'images downloaded from the class', class_name, 'check your class folder.')
                
def get_images_of(class_name):
    url = "https://www.google.com.br/search?q="+class_name+"&prmd=inv&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj3mdzbnrXZAhWQuFMKHY7DAbYQ_AUIESgB#imgrc=_"
    path_webdriver = "C:\\webdrivers\\chromedriver.exe"
    driver = webdriver.Chrome(path_webdriver)
    driver.get(url)

    print("Get a coffe, while I search the images for you")
    jump_size = 200
    for i in range(20):
        base_jump = 1000
        driver.execute_script('window.scrollTo(0, '+str(base_jump + jump_size)+');')
        jump_size += 200
        time.sleep(1)
        
    html = driver.page_source
    bsobj = BeautifulSoup(html, 'html5lib')
    image_list = bsobj.findAll('img',{'class':'rg_ic rg_i'})

    image_src_list = []
    for image in image_list:
        try:
            image_src_list.append(image.attrs['src'])
        except:
            print('failed to found the source of', image)
    driver.close()
    print(len(image_src_list),'found, starting the download!')
    download_images(class_name, image_src_list)

message = """
        GOOGLE IMAGES SCRAPPER
        Initializing search...
"""
print(message)
get_images_of('ferrari')
