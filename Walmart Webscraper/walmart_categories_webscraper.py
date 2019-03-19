
from selenium import webdriver
import selenium.webdriver.support.ui as UI
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import pandas as pd
import numpy as np
import re
import time
import math
import json
import datetime
import ast


# Create data frame
columns = ['Category', 'Subcategory', 'AisleID']

df = pd.DataFrame(columns=columns)


# Open web browser
chrome_path = r"I:\Python\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver2 = webdriver.Chrome(chrome_path)


# Get store id
zipcode = 50305
driver.get('https://grocery.walmart.com/v2/api/serviceAvailability?postalCode='+str(zipcode))
storeid = re.search('storeId\"\:\"(\d+)\"', driver.find_element_by_xpath("""/html/body/pre""").text).group(1)


# Enter in zip code
driver.get('https://grocery.walmart.com/')
time.sleep(1)
driver.find_element_by_xpath("""//*[@id="postalCode"]""").send_keys(zipcode)


# Click on "Check Availability"
driver.find_element_by_xpath("""/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div/form/div/button""").click()


# Click on "Start Shopping"
driver.find_element_by_xpath("""/html/body/div[2]/div/div/div/div[2]/button""").click()


# Click on "Shop by department"
driver.find_element_by_xpath("""/html/body/div[1]/div/div[2]/div[1]/div/div/div/header/div[1]/button/span""").click()
category_list = driver.find_elements_by_xpath("""/html/body/div[1]/div/div[2]/div[1]/div/div/div/header/nav/div/section/ul/li""")

for x in range(0, len(category_list)):
    category = category_list[x].find_element_by_xpath("""./button/div""").text
    actions = ActionChains(driver)
    actions.move_to_element(category_list[x]).perform()
    time.sleep(1)
    category_list[x].click()
    time.sleep(1)
    sub_cat_list = driver.find_elements_by_xpath("""/html/body/div[1]/div/div[2]/div[1]/div/div/div/header/nav/div/section[2]/ul/li""")
    for y in range(0, len(sub_cat_list)):
        subcategory = sub_cat_list[y].find_element_by_xpath("""./a""").text
        aisleid = re.search('\d+_\d+', sub_cat_list[y].find_element_by_xpath("""./a""").get_attribute('href')).group(0)
        df = df.append(pd.Series([category, subcategory, aisleid], index=columns), ignore_index=True)


writer = pd.ExcelWriter('WalmartCategories.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()