
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
columns = ['Source', 'Category', 'SubCategory', 'SKU', 'ProductName', 'MaxAllowed', 'TaxCode', 'IsOutofStock',
          'Image', 'IsAlcoholic', 'PrimaryShelfID', 'PrimaryShelfName', 'PrimaryDepartmentID', 'PrimaryDepartmentName',
          'VendorPackQuantity', 'VendorPackVolume', 'VendorPackWeight', 'SalesUnit', 'AverageWeight',
          'StorePriceisClearance', 'StorePriceisRollback', 'StorePriceList', 'StorePriceUnitofMeasure',
          'StoreSalesQuantity', 'StoreSalesUnitofMeasure', 'StoreDisplayPrice', 'StoreDisplayUnitPrice']

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
    category_list[x].click()
    time.sleep(1)
    sub_cat_list = driver.find_elements_by_xpath("""/html/body/div[1]/div/div[2]/div[1]/div/div/div/header/nav/div/section[2]/ul/li""")
    for y in range(0, len(sub_cat_list)):
        subcategory = sub_cat_list[y].find_element_by_xpath("""./a""").text
        aisleid = re.search('\d+', sub_cat_list[y].find_element_by_xpath("""./a""").get_attribute('href')).group(0)
        driver2.get('https://grocery.walmart.com/v2/api/products?strategy=aisle&returnFilters=true&itemFields=basic&itemFields=store&taxonomyNodeId='+aisleid+'&storeId='+storeid+'&count=500&offset=0')
        productjson = json.loads(driver2.find_element_by_xpath("""/html/body/pre""").text)
        for product in productjson['products']:
            sku = product['sku']
            productName = product['basic']['name']
            maxAllowed = product['basic']['maxAllowed']
            taxCode = product['basic']['taxCode']
            isOutofStock = product['basic']['isOutOfStock']
            try:
                image = product['basic']['image']['large']
            except:
                image = ''
            isAlcoholic = product['basic']['isAlcoholic']
            primaryShelfID = product['basic']['primaryShelf']['id']
            primaryShelfName = product['basic']['primaryShelf']['name']
            primaryDeptID = product['basic']['primaryDepartment']['id']
            primaryDeptName = product['basic']['primaryDepartment']['name']
            vendorPackQuant = product['basic']['vendorPack']['quantity']
            try:
                vendorPackVol = product['basic']['vendorPack']['volume']
            except:
                vendorPackVol = ''
            try:
                vendorPackWeight = product['basic']['vendorPack']['weight']
            except:
                vendorPackWeight = ''
            salesUnit = product['store']['price']['unit']
            avgWeight = product['basic']['averageWeight']
            isClearance = product['store']['price']['isClearance']
            isRollback = product['store']['price']['isRollback']
            storePriceList = product['store']['price']['list']
            storePriceUnitofMeasure = product['store']['price']['priceUnitOfMeasure']
            storeSalesQuant = product['store']['price']['salesQuantity']
            storeSalesUnitofMeasure = product['store']['price']['salesUnitOfMeasure']
            storeDisplayPrice = product['store']['price']['displayPrice']
            try:
                storeDisplayUnitPrice = product['store']['price']['displayUnitPrice']
            except:
                storeDisplayUnitPrice = ''
            df = df.append(pd.Series(['Walmart', category, subcategory, sku, productName,
                                     maxAllowed, taxCode, isOutofStock, image, isAlcoholic,
                                     primaryShelfID, primaryShelfName, primaryDeptID, primaryDeptName,
                                     vendorPackQuant, vendorPackVol, vendorPackWeight, salesUnit,
                                     avgWeight, isClearance, isRollback, storePriceList, storePriceUnitofMeasure,
                                     storeSalesQuant, storeSalesUnitofMeasure, storeDisplayPrice,
                                      storeDisplayUnitPrice], index=columns), ignore_index=True)


writer = pd.ExcelWriter('WalmartCPI.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

