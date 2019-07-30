# -*- coding: utf-8 -*-
import argparse
import json
import requests
import re
import os
from itertools import chain 
def getJson(url):
    # http = re.PoolManager()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    response = requests.get(url, headers = headers)
    jsObj = response.json()
    print("url:{}\nstatus:{}".format(url,response.status_code))

    # print(jsObj)
    return jsObj

def getContent(data):
    return data['content']

def getNextPage(paging):
    return paging['paging']['next']

def getPrevPage(paging):
    return paging['paging']['previous']

def isLastPage(jsonObject):
    isEnd = jsonObject['paging']['is_end']
    print("isEnd",isEnd)
    return isEnd   

def getDataList(jsonObject):
    return jsonObject['data']

def download(imgUrl, dir):
    from urllib.request import urlretrieve

    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
        #文件名 忽略前十个字符
        name = imgUrl[30:]
    except IOError as e:
        print(e.getContent) 

    urlretrieve(imgUrl, filename = dir+"/"+name)


def getContentImg(html):
    replace_pattern = r'<[img|IMG].*?/>' #img标签的正则式
    img_url_pattern = r'.+?src="(\S+)"' #img_url的正则式
    img_url_list = []
    need_replace_list = re.findall(replace_pattern, html)#找到所有的img标签
    for tag in need_replace_list:
        if(len(re.findall(img_url_pattern, tag))>0):
            img_url_list.append(re.findall(img_url_pattern, tag)[0])#找到所有的img_url
    print('imageUrls:',img_url_list)    
    return img_url_list    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-answer")
    args = parser.parse_args()
    pageNo = 1
    pageSize = 20
    # https://www.zhihu.com/api/v4/questions/295119062/answers?include=data%5B%2A%5D.is_normal%2Ccontent&limit=3&offset=3
    url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Ccontent&limit={}&offset={} "
    answer = args.answer
    isLast = False


    #图片列表
    imgList = []

    jsonObject = getJson(url.format(answer, pageSize, pageNo))
    while isLast == False:
        for data in getDataList(jsonObject):
            imgList.append(getContentImg(getContent(data)))
        print("开始处理下一页")    
        jsonObject = getJson(getNextPage(jsonObject))
        isLast = isLastPage(jsonObject)   

    
    for img in list(chain.from_iterable(imgList)):
        print("下载:",img)
        download(img,"./images")    
