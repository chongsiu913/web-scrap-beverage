from distutils.log import info
from lib2to3.pgen2 import driver
from bs4 import BeautifulSoup
from tabulate import tabulate
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def web_scrap(shop_desc, url):

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.implicitly_wait(2) # seconds
    driver.get(url)

    for x in range(10):
        try:
            showMoreButton = driver.find_element_by_class_name("showMore ")
            showMoreButton.click()
            time.sleep(1)
            print('found showMore button')
        except:
            print('canot find showMore button')

    pageSource = driver.page_source        
    soup = BeautifulSoup(pageSource,'lxml')

    item_regex = re.compile('.*item.*')
    all_items = soup.find_all('div',{"class" : item_regex})
    
    # user variable
    cannot_find_desc = 'N/A'
    item_array_for_print = []
    
    for item in all_items:
        array = []

        # source info
        item_source = shop_desc
        item_source_url = url
        #  name of the item
        item_name = cannot_find_desc
        item_name_container = item.find('div',class_='name')
        if item_name_container is not None:
            item_name = item_name_container.find('p').text
        else:
            continue
            
        # volumn of the item
        item_volumn = cannot_find_desc
        item_volumn_container = item.find('div',class_='volumn')
        if item_volumn_container is not None:
            item_volumn = item_volumn_container.find('span',class_='sizeUnit').text
        
        # prize
        item_normal_prize = cannot_find_desc
        item_discount_prize = cannot_find_desc

        item_prize_container = item.find('div',class_='price-container')
        if item_prize_container is not None:
            item_normal_prize_container = item_prize_container.find('div',class_='price rrp newPrice')
        
            
            if item_normal_prize_container is not None:
                if item_normal_prize_container.find('span') is not None:
                    item_normal_prize = item_normal_prize_container.find('span').text
        
                

            item_discount_prize_container = item_prize_container.find('div',class_='price discount newPrice')
            if item_discount_prize_container is not None:
                item_discount_prize = item_discount_prize_container.text

        # special offer
        item_sp_offer = cannot_find_desc
        item_sp_off_container = item.find('div', class_='special-offer special-offerStyle')
        if item_sp_off_container is not None:
            item_sp_offer = item_sp_off_container.find('span').text
        
            
        
        array += [item_source] + [item_source_url] + [item_name] + [item_volumn] + [item_normal_prize] + [item_discount_prize] + [item_sp_offer]

        item_array_for_print.append(array)
        # print(item_array_for_print)
    return item_array_for_print
    
    # print(tabulate(item_array_for_print, headers=['Source','Source URL','Name','Volumn','Normal Prize','Discount Prize','Special Offer']))
    # print('Total item: ' + str(len(item_array_for_print)))