from selenium import webdriver
from app.api.data_getter import nohead_browser, taobaoLogin, kandianbaoLogin
from bs4 import BeautifulSoup
import time
import re
from app.database.database import SessionLocal, Base, engine
from app.database.models import Shops
import os
import random
from datetime import datetime

dccURL = 'https://www.dianchacha.com/shop/info/index/uid/' + 'shopID'

def randomKeyWord():
    """ Read itemscate file into array """
    fo = open(os.getcwd() + '/app/api/data_getter/itemscate.txt', 'r')
    words = fo.read().splitlines()
    return words[random.randint(0,len(words)-1)]

def getTaobaoShopSoup(keyWord, username, password):
    driver = nohead_browser.setBrowser(username, isMitmProxy=False)
    driver.get(
        "https://shopsearch.taobao.com/search?q="
        + keyWord
        + '&sort=credit-desc&s=1980&ratesum=xin'
    )
    time.sleep(3)
    if keyWord not in driver.title:
        driver = taobaoLogin.Login(username, password, driver).start()
        if type(driver) == str:
            # Raise Login Error
            return {'message': driver, 'code': '74147'}
    driver.get(
        "https://shopsearch.taobao.com/search?q="
        + keyWord
        + '&sort=credit-desc&s=1980&ratesum=xin'
    )
    driver.execute_script("window.scrollBy(0,3000)")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,3000)")
    time.sleep(1)
    content = driver.page_source.encode('utf-8')
    driver.close()
    return content

def getShopListFromTaobaoSoup(driverContent):
    soup = BeautifulSoup(driverContent, 'lxml')
    # soup = soup.find('shopsearch-shoplist')
    soup = soup.find('ul', id='list-container')
    if soup == None:
        return 'Login Error'
    pattern = re.compile(r'&fromid=.+')
    for item in soup.select(".list-info"):
        try:
            shopH4 = item.find('h4')
            shopName = str(shopH4.a.string).replace(' ','').replace('\n','')
            shopUrl = 'https:' + shopH4.a['href']
            shopInfoList = item.select('.shop-info-list')[0]
            sellerName = str(shopInfoList.a.string).replace(' ','').replace('\n','')
            sellerUrl = 'https:' + shopInfoList.a['href']
            sellerUid = str(shopInfoList.a['trace-uid']).replace(' ','').replace('\n','')
            wangwangInfo = item.select('.ww-inline')[0]
            sellerWangWangIsOnline = str(wangwangInfo.span.string).replace(' ','').replace('\n','')
            sellerWangWangUrl = str(wangwangInfo['href']).replace(pattern.findall(wangwangInfo['href'])[0], '')
            valuation = item.select('.valuation')[0]
            goodCommentRatio = str(valuation.select('.good-comt')[0].string).replace(' ','').replace('\n','')
            isConsumerInsure = str(valuation).find('消费者保障') != -1
            isGoldenSeller = str(valuation).find('金牌卖家') != -1
        except IndexError:
            raise("Taobao Data Grasp Error")
        except AttributeError:
            raise("CSS Selector Error")
        shop = Shops(shopName=shopName, shopURL=shopUrl, sellerName=sellerName, \
            sellerURL=sellerUrl, sellerUid=sellerUid,sellerWangWangOnlineStatus = sellerWangWangIsOnline,\
            sellerWangWangURL=sellerWangWangUrl, goodCommentRatio=goodCommentRatio,\
            isConsumerInsure=isConsumerInsure, isGoldSeller =isGoldenSeller)
        session = SessionLocal()
        isSellerExist = session.query(Shops).filter(Shops.sellerUid == sellerUid).first()
        if not isSellerExist:
            session.add(shop)
        session.commit()
    session.close()
    return 0
        
def queryUncompleteShop():
    session = SessionLocal()
    wangwangName = session.query(Shops).filter(Shops.numberOfFans == -1).first().sellerName
    if wangwangName:
        return wangwangName
    else:
        message = '请获取更多淘宝店铺'
        return message
    
def getKandianbaoShopInfoSoup(wangwangName, username, password, driver):
    driver.get('https://kandianbao.com/dian/' + wangwangName)
    if wangwangName not in driver.title:
        driver = kandianbaoLogin.Login(driver, username, password).login()
        if type(driver) == str:
            message = driver
            return message
        driver.get('https://kandianbao.com/dian/' + wangwangName)
    time.sleep(3)
    if wangwangName not in driver.title:
        message = '限额已耗尽'
        driver.close()
        return message
    content = driver.page_source.encode('utf-8')
    return [content, driver]

def getShopInfoFromKDBSoup(wangwangName, driverContent):
    soup = BeautifulSoup(driverContent, 'lxml')
    mt10 = soup.select('.mt10')[0].find('tbody')
    mt10Dic = {
        '店铺粉丝数':0,
        '所在地区': None,
        '店铺宝贝数': 0,
        '创店时间': None,
        'DSR': 0,
        '主营类目': None
    }
    for row in mt10.find_all('tr'):
        for col in row.children:
            curGrid = str(col.string)
            if curGrid in mt10Dic:
                for elem in col.next_siblings:
                    if str(elem).find('<td>') != -1:
                        allString = ''
                        for string in elem.stripped_strings:
                            allString += string
                        mt10Dic[curGrid] = allString
                        break
    pattern = re.compile(r'[\d]+')
    mt10Dic['店铺宝贝数'] = pattern.findall(mt10Dic['店铺宝贝数'])[0]
    if mt10Dic['所在地区'] == '':
        mt10Dic['所在地区'] = '-'
    session = SessionLocal()
    shop = session.query(Shops).filter(Shops.sellerName == wangwangName).first()
    shop.numberOfFans = mt10Dic['店铺粉丝数']
    shop.shopZone = mt10Dic['所在地区']
    shop.numberOfItems = mt10Dic['店铺宝贝数']
    shop.openingDate = (datetime.strptime(mt10Dic['创店时间'], '%Y-%m-%d %H:%M:%S'))
    shop.dsr_value = mt10Dic['DSR']
    shop.shopCategory = mt10Dic['主营类目']
    session.commit()
    return 0

def writeDataIntoFile(file, data):
    fo = open(file, 'wb')
    fo.write(data)
    fo.close()

def readDataFromFile(file):
    fo = open(file, 'rb')
    data = fo.read()
    fo.close()
    return data

def startTaobaoCollector(account, password):
    driverContent = getTaobaoShopSoup(randomKeyWord(), account)

# if __name__ == "__main__":
    # print(readItemscate())
    # print(randomKeyWord(readItemscate()))
    # driverContent = getTaobaoShopSoup("电源", "testuser")
    # writeDataIntoFile('./test/driver_content', driverContent)
    # driverContent = readDataFromFile('./test/driver_content')
    # getShopListFromTaobaoSoup(driverContent)
    # driver = nohead_browser.setBrowser('testuser', isMitmProxy=False)
    # while (queryUncompleteShop()):
    #     wangwangName = queryUncompleteShop()
    #     SoupAndDriver = getKandianbaoShopInfoSoup(wangwangName, 'testuser', driver)
    #     writeDataIntoFile('./test/kandianbao_driver_content', SoupAndDriver[0])
    #     driverContent = readDataFromFile('./test/kandianbao_driver_content')
    #     getShopInfoFromKDBSoup(queryUncompleteShop(), driverContent)
