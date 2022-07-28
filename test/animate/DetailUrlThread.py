from array import array
from threading import Thread
import re

from bs4 import BeautifulSoup
import requests
from lxml import etree
import os
import datetime

import utils

""" 通过详细网址爬取详细网页信息进而启动下载 """
class DetailUrlThread(Thread):
    """ 爬取详细网址信息的线程 """

    def __init__(self, urlList, sem,savePath):
        """ DetailUrlThread的初始化方法 """
        super().__init__()
        self.urlList = urlList
        self.sem = sem
        self.savePath =  savePath#utils.seedFilePath
        # print("当前任务下载地址："+self.savePath)
        self.downloadInfos = []

        
    def run(self):
        num =1
        for url in self.urlList:
            print("总共需要处理{}个资源，目前以进行{}个".format(len(self.urlList),num))
            num = num + 1
            downloadInfo = self.getDownloadInfo(url)
            #print(downloadInfo)
            if downloadInfo == None:
                continue
        
            # 开始信号量锁
            self.sem.acquire()

            # 多线程开始下载
            self.startDownload(downloadInfo)

            # 将所有下载信息添加到列表中
            self.downloadInfos.append(downloadInfo)
            
    def startDownload(self, downloadInfo):
        downloadThread = DownloadThread(downloadInfo,self.sem,self.savePath)
        downloadThread.start()

    def getDownloadInfo(self, url):
        """ 获取单个文件的信息 """
        detailResponse = utils.requestsGet(url)
        if(detailResponse == None):
            print("请求页面失败")
            return None
        soup = utils.soupGet(detailResponse.text)
        contentInfos = soup.select("#btm > div.main > div > div")
        contentInfoText = contentInfos[0].get_text()
        if contentInfoText == "种子文件不存在！":
            print("页面异常,没有种子,网址是: {}".format(url))
            return None

        downloadInfos = soup.select("#download")

        downloadUrl = ""
        if len(downloadInfos) > 0:
            href = downloadInfos[0].get("href")
            downloadUrl = utils.baseURL + href

        '''
        href的格式:
        down.php?date=1556390414&hash=d8e9125797a795c6888e62b6f952b5d6e38265ba
        '''
        # 获取详细页面的标题
        infos = soup.select("#btm > div.main > div.slayout > div > div.c2 > div:nth-child(2) > div.torrent_files > ul > li > img")
        if len(infos) > 0:
            title = infos[0].nextSibling
        else:
            title = "标题没有成功获取"
 
        # 通过字符串分割获取时间戳和哈希值
        dateAndHash = ""
        hrefInfos = href.split(sep = "?")
        if len(hrefInfos) > 1:
            dateAndHash = hrefInfos[1]

        # 获取时间戳
        date = self.getDetailUrlOfDate(dateAndHash)

        # 获取哈希值
        hashValue = self.getDetailUrlOfHashValue(dateAndHash)

        # 获取文件大小
        size = self.getDetailUrlOfSize(soup)

        # 获取字符串的基本信息
        #basicInfo = self.getDetailUrlOfBasicInfo(detailResponse.text, soup)

        # 生成下载信息模型
        timeStamp = int(date)
        if timeStamp == None:
            s = datetime.datetime.now
        else:
            dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
            s = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        downloadInfo={"title": title, "downloadUrl": downloadUrl, "date": date, "hashValue": hashValue, "size": size,"time":s}
        return downloadInfo


    def getDetailUrlOfSize(self, soup) -> str:
        """ 获取详细页面的文件大小 """
        infos = soup.select("#btm > div.main > div.slayout > div > div.c2 > div:nth-child(2) > div.torrent_files > ul > li > span")
        size = ""
        if len(infos) > 0:
            text = infos[0].get_text()
            size = text.replace("(","").replace(")","")
        else:
            size = "文件大小未成功获取"
        return size

    def getDetailUrlOfDate(self, dateAndHash) -> str:
        """ 获取详细页面的种子时间戳 """
        # date = dateAndHash.split(sep = "&")[0].split(sep = "=")[1]
        arrayFirstDateAndSceondHash = dateAndHash.split(sep = "&")
        date = "时间戳未获取成功"

        if len(arrayFirstDateAndSceondHash) > 0:
            dateInfo = arrayFirstDateAndSceondHash[0]
            dateValue = dateInfo.split(sep = "=")
            if len(dateValue) > 1:
                date = dateValue[1]
                return date

        return date

    def getDetailUrlOfHashValue(self, dateAndHash) -> str:
        """ 获取详细页面的种子的哈希值 """
        #hashs = dateAndHash.split(sep = "&")[1].split(sep = "=")[1]
        arrayFirstDateAndSceondHash = dateAndHash.split(sep = "&")
        hashs = "哈希值未获取成功"

        if len(arrayFirstDateAndSceondHash) > 1:
            hashInfo = arrayFirstDateAndSceondHash[1]
            hashValue = hashInfo.split(sep = "=")
            if len(hashValue) > 1:
                hashs = hashValue[1]
                return hashs
        return hashs

    """ 元组的返回是不能 -> (str, str)这么写的 """
    def getDetailUrlOfBasicInfo(self, htmlText, soup):
        """ 获取详细页面的基本信息 """
        selector = etree.HTML(htmlText)
        string = selector.xpath('//*[@id="btm"]/div[10]/div[2]/div/div[1]/div[1]/div/p[6]/text()')
        info = soup.select("#btm > div.main > div.slayout > div > div.c1 > div:nth-child(1) > div > p:nth-child(6)")[0].get_text()
        return (string, info)


class DownloadThread(Thread):
    """ 下载的线程 """
    def __init__(self, downloadInfo, sem,savePath):
        super().__init__()
        self.downloadInfo = downloadInfo
        self.name = downloadInfo["title"] + ".torrent" 
        self.sem = sem
        self.savePath = savePath
        self.seedFiles = []
        # 获取下载目录下的所有文件
        for _, _, files in os.walk(self.savePath):  
            self.seedFiles = files
            #print("当前目录下的文件有:{}".format( self.seedFiles))

    def run(self):
        if self.name in self.seedFiles:
            print("已有{}文件,直接返回".format(self.name))
        else:
            print("下载文件: {}".format(self.downloadInfo["title"]))
            self.download(self.downloadInfo["downloadUrl"], self.name)

        # 解开信号锁
        self.sem.release()

    def download(self, downloadURL, name):
        """ 进行下载请求 """
        response = utils.requestsPost(downloadURL)
        data = response.content
        print(self.savePath +'\\'+name)
        try:
            with open(self.savePath +'\\'+name,"wb") as f:
                f.write(data)
            print("下载完成: {}".format(name))
        except:
            print("下载失败: {}".format(name))
