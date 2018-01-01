# -*- coding: utf-8 -*-
# version python3.6

from urllib import request
from bs4 import BeautifulSoup as bs
import csv

def getList():
    resp = request.urlopen('https://movie.douban.com/nowplaying/beijing/')
    html_data = resp.read().decode('utf-8') 

    soap = bs(html_data, 'html.parser')
    nowplaying_movie = soap.find_all('div', id = 'nowplaying') 
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_ = 'list-item')
    
    return nowplaying_movie_list

def getComments(id):
    requrl = "https://movie.douban.com/subject/" + id + "/comments?start=0&limit=20"
    resp = request.urlopen(requrl)
    html_data = resp.read().decode('utf-8')

    soap = bs(html_data, 'html.parser')
    title = soap.find('title')
    comment_div_list = soap.find_all('div', class_ = 'comment')
    commentList = []
    for cm in comment_div_list:
        if cm.find_all('p')[0] is not None:
            try:
                commentListDetail = []
                commentListDetail.append(title.string[:-3].strip())
                commentListDetail.append(cm.find_all('span', class_='comment-info')[0].find('span', class_='rating')['title'].strip())
                commentListDetail.append(cm.find_all('p')[0].string.strip().replace(",", " ").replace("£¬", " "))
                
                commentList.append(commentListDetail)
            except:
                continue
          
    return commentList

def list2csv(list, file):
    wr = csv.writer(open(file,'w', encoding = 'utf-8'), quoting=csv.QUOTE_ALL)
    for movie in list:
        for word in movie:
            print (word)
            wr.writerow(word)
        
def writeFile(codeList):
    i=0
    sumList = []
    for code in codeList:
        i = i+ 1
        print (i)
        if i > 10:
            print ("end")
            break
        infoDict = getComments(code['data-subject'])
        if infoDict is None:
            continue
        sumList.append(infoDict)
    
    list2csv(sumList, 'E://Data2.csv')
    
movie_list = getList()
writeFile(movie_list)