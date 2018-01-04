# -*- coding: utf-8 -*-
# version python3.6

from urllib import request
from bs4 import BeautifulSoup as bs
import csv
import random

base_url = 'https://www.amazon.com'

def setRequest(req, url):
    headers=["text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"]
    randdom_header=random.choice(headers)
    req.add_header("User-Agent",randdom_header)
    req.add_header("Host","www.amazon.com")
    req.add_header("Referer","https://www.amazon.com/")
    req.add_header("GET",url)

def getList():
    global base_url
    i = 1
    url_list = []
    url_0 ='/s/ref=sr_1_1_hso_sc_smartcategory_3/133-4270117-5105935?rh=n%3A2407749011%2Ck%3Aphone&amp;keywords=phone&amp;ie=UTF8&amp;qid=1514992192&amp;sr=8-1-acs';

    while i <= 8:
        try:
            url = base_url + url_0
            print ('page num', str(i), url)
            req=request.Request(url)
            setRequest(req, url)
            resp_text=request.urlopen(req).read()
            soap = bs(resp_text, 'html.parser')

            try:
                for j in range(24*(i-1), i*24):
                    if j == 0:
                        continue
                    tid = 'result_' + str(j)
                    print ('   ', str(j))
                    phone_url = soap.find('li', id = tid).find_all('div', class_='a-fixed-left-grid-col')[1].find_all('div', class_='a-spacing-small')[0].find('a')['href']
                    print ('           ', phone_url)
                    url_list.append(phone_url)


                url_0 = soap.find('a', id = 'pagnNextLink')['href']
            except Exception as e:
                print (e)
                continue
            i = i + 1
        except :
            continue
    print (len(url_list))

    return url_list

def getComments(href, id):
    global base_url

    requrl = href;
    req=request.Request(requrl)
    setRequest(req, requrl)
    resp_text=request.urlopen(req).read()

    soap = bs(resp_text, 'html.parser')
    product_name = soap.find('span', id='productTitle')
    comment_div_list = soap.find('div', id='cm-cr-dp-review-list').find_all('div', class_='a-section review')
    commentList = []

    #     print (requrl)
    for cm in comment_div_list:
        try:
            commentListDetail = []
            commentListDetail.append(id)
            commentListDetail.append(product_name.string.strip())
            commentListDetail.append(cm.find_all('span', class_='a-icon-alt')[0].string.strip()[:3])
            commentListDetail.append(cm.find_all('div', class_='a-expander-partial-collapse-content')[0].string.strip().replace(",", " ").replace("，", " "))
            #             print (commentListDetail)
            commentList.append(commentListDetail)
        except Exception as e:
            print ('get comment error====', e)
            continue

    return commentList

def list2csv(list, file):
    wr = csv.writer(open(file,'w', encoding = 'utf-8'), quoting=csv.QUOTE_ALL)
    wr.writerow(['id','name','score','comment'])
    for movie in list:
        for word in movie:
            print (word)
            wr.writerow(word)

def writeFile(url_list):
    i=0
    sumList = []
    for href in url_list:
        i = i+ 1
        print ('num->',i)
        if i > 30:
            print ("end")
            break

        try:
            print ('write=====',href)
            infoDict = getComments(href, href[href.index('dp/')+3 : href.index('dp/')+13])

            if infoDict is None:
                continue
            #             print (infoDict)
            sumList.append(infoDict)
        except Exception as e:
            print ('write error====', e)
            continue

    list2csv(sumList, 'E://Data2.csv')

url_list = getList()
print ('start--------')
writeFile(url_list)