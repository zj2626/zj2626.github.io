# version python3.6

from urllib import request
from bs4 import BeautifulSoup as bs
import re
import csv

baseUrl = 'http://bj.ganji.com'

def getCodes():
    global baseUrl
    url = baseUrl + '/fang1/';
    resp = request.urlopen(url)
    resp_text = resp.read()
    soap = bs(resp_text, 'html.parser')
    list = soap.find_all('div', class_ = 'f-main-list')[0].find_all('div', class_ = 'ershoufang-list')

    codeList = []
    for li in list:
        try:
            url = li.find('div', class_ = 'img-wrap').find('a')['href']
            len = url.index('?')
            codeList.append(url[: len])
        except:
            continue

    return codeList

def makeDict(code):
    global baseUrl
    infoDict = {}
    url = '%s%s' % (baseUrl, code)
    try:
        print (url)
        resp = request.urlopen(url)
        resp_text = resp.read()
        soap = bs(resp_text, 'html.parser')

        stockInfo = soap.find_all('div', class_ = 'card-top')
        # 房源title
        infoDict['房源'] = soap.find('p', class_ = 'card-title').find('i').string
        # 房租
        infoDict['房租'] = soap.find('ul', class_ = 'card-pay').find('li', class_ = 'price').find('span', class_ = 'num').string
        houseInfo = soap.find('ul', class_ = 'er-list').find_all('li', class_ = 'item')
        # 户型
        infoDict['户型'] = houseInfo[0].find('span', class_ = 'content').string
        # 面积
        infoDict['面积'] = re.sub("\D", "", houseInfo[1].find('span', class_ = 'content').string)
        # 朝向
        infoDict['朝向'] = houseInfo[2].find('span', class_ = 'content').string
        # 楼层
        infoDict['楼层'] = re.sub("\D", "", houseInfo[3].find('span', class_ = 'content').string)
        #装修情况
        infoDict['装修情况'] = houseInfo[4].find('span', class_ = 'content').string

        return infoDict
    except Exception as e:
        print (e)
        return None

def dict2csv(dictList,file):
    with open(file,'w', encoding = 'utf-8') as f:
        w=csv.writer(f)
        w.writerow(dictList[0].keys())
        for dict in dictList :
            w.writerow(dict.values())

def writeFile(codeList):
    i=0
    sumList = []
    for code in codeList:
        i = i+ 1
        print (i)
        if i > 24:
            print ("end")
            break
        infoDict = makeDict(code)
        if infoDict is None:
            continue
        print (infoDict)
        sumList.append(infoDict)

    dict2csv(sumList, 'E://GraphLabData/Data.csv')

codeList = getCodes();
print("start")
writeFile(codeList)