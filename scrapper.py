# -*- coding: utf-8 -*-
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, os, threading

class ImageScrapper(threading.Thread):

    def __init__(self, class_name, quant_images):
        """
        ============================================
        initialize the class_name and the quantity
        of images to download
        ============================================
        """
        threading.Thread.__init__(self)
        self.class_name = class_name
        self.quant_images = quant_images
        self.max_images = 200
        self.max_string_size = 30
        if self.quant_images > self.max_images:
            print('Maximum of images is %s' % self.max_images)
            
        
    def download_images(self, image_src_list):
        """
        ============================================
        get a list of images and use urlretrieve to
        try download every image in hte list
        ============================================
        """
        
        repo_name = self.class_name
        try:
            os.mkdir(repo_name)
        except:
            repo_name = self.class_name+'-'+str(time.time())
            os.mkdir(repo_name)
        
        images_downloaded = 0
        for index, image_src in enumerate(image_src_list):
            try:
                urlretrieve(image_src, repo_name+"/"+self.class_name+str(index)+'.jpg')
                # print('download [OK]: %s...' % image_src[:self.max_string_size])
                images_downloaded += 1
            except:
                print('download [FAILED]: %s...' % image_src[:self.max_string_size])    
            if index == self.quant_images - 1 or index == self.max_images - 1: break
            
        print('%s images downloaded from the class %s check your class folder.' % (str(images_downloaded), self.class_name))
                    
    def run(self):
        """
        ============================================
        receive a class name that will be used for
        search images using google images tool
        ============================================
        """
        
        url = "https://www.google.com.br/search?q="+self.class_name+"&prmd=inv&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj3mdzbnrXZAhWQuFMKHY7DAbYQ_AUIESgB#imgrc=_"
        path_webdriver = "C:\\webdrivers\\chromedriver.exe"
        driver = webdriver.Chrome(path_webdriver)
        driver.get(url)
        
        print("Get a coffe, while I search the images for you")

        # IMPORTANT!: the scrolls are necessary to render more images on the screen for scrap
        base_jump, jump_size = 1000, 200
        for i in range(20):
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
                print('failed to found the source of %s...' % image.get_text()[:self.max_string_size])
            
        driver.close()
        print('%s found, starting the download!' % str(len(image_src_list)))
        self.download_images(image_src_list)

"""
Usage example zone
"""
# TESTING THE DIFFERENCE BETWEEN NON HEADLESS AND HEADLESS WEBDRIVERS
classes = ['ferrari', 'lamborghini', 'volkswagen']
threads = []

for classe in classes: threads.append(ImageScrapper(classe, 10))
for thread in threads: thread.start()
for thread in threads: thread.join()
