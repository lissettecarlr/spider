
import os
import Formate
import requests
from bs4 import BeautifulSoup
import random
import sys
import re
from threading import Semaphore
from DetailUrlThread import DetailUrlThread
import utils
import csv
from lxml import etree

# userAgent
userAgent = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
# 请求头
headers = {"User-Agent": random.choice(userAgent),
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}


def startSearch(keyword):
    # 对关键字进行搜索，得到各类信息
    (soup, htmlText) = searchAnimation(keyword = keyword)

    # 该关键字搜索出的页码
    pageNum = getSearchPageNum(soup)
    print("关键字: " + keyword + " 共有 " + str(pageNum) + " 页")
    if pageNum == None:
        print("search :"+ keyword+ " not find !")
        return

    # 该关键字搜索出的数据总数
    resultCountInfos = soup.select("#btm > div.main > div > h2 > span")
    resultCountText = resultCountInfos[0].get_text()
    # 使用正则获取其中的数字
    resultCounts = re.search(r"\d+",resultCountText)
    resultCount = resultCounts.group()
    if resultCount == 0 or resultCount == None:
        print("该页面没用资源.")
        return
    print("共搜索出资源：{}".format(resultCount))
  
    
    seedFilePath = os.path.dirname(os.path.realpath(sys.argv[0]))    
    savePath = seedFilePath + "\\" + keyword
    csvFile = savePath + "\\" + keyword + ".csv"
    
    # 判断文件夹是否存在,如果不存在就创建一个
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    if(os.path.exists(csvFile)):
        try:
            os.remove(csvFile)
        except:
            print("删除文件失败")
    else:
        pass


    for page in range(1, int(pageNum)+1):
        if(page != 1):
            (soup, htmlText) = searchAnimation(keyword,page)
            
        downInfo = searchAction(soup,seedFilePath + "\\" + keyword)
        print("第{}页 处理完成".format(page))

        if len(downInfo) == 0 or downInfo == None:
                return
        else:
            for info in downInfo:
                try:
                    with open (csvFile, "a+") as fp:
                        writer = csv.writer(fp)
                        writer.writerow((info["title"], info["downloadUrl"], info["time"], info["size"]))
                except IOError as error:
                    print(error)
                finally:
                    pass

# 传入搜索关键字，然后返回搜索后的页码
def getSearchPageNum(soup) -> int:

    # 保存搜索出来的类容
    listInfos = soup.select("#data_list > tr > td")
    if len(listInfos) > 0:
        text = listInfos[0].get_text()
        if text == "没有可显示资源":
            print(text)
            return None

    #但页码过多时需要用这个 例如： 1 2 3 4 5 .....  12
    pageLastInfos = soup.select("#btm > div.main > div.pages.clear > a.pager-last.active")
    #但页码数量少时，匹配pages.clear的第三个元素
    pageInfos = soup.select("#btm > div.main > div.pages.clear > a:nth-child(3)")
    # print(pageLastInfos)
    # print(pageInfos)

    if pageLastInfos == None and pageInfos == None:
        print("没获取到页码")
        return None

    if len(pageLastInfos) > 0:
        pageNum = pageLastInfos[0].get_text() or 1
        return pageNum
    elif len(pageInfos) > 0:
        pageNum = pageInfos[0].get_text() or 1
        return pageNum
    else:
        return 1


def searchAnimation(keyword , pageNum = None):
    """ 通过关键词搜索 返回搜索页的soup """
    if pageNum == None :
        pageNum =1 
    page = Formate.pageFormate(pageNum)
    keyword = Formate.keywordFormat(keyword)
    keywordURL = utils.baseURL + keyword + page
    try:
        keywordResponse = requests.get(keywordURL, headers = headers,timeout=10)
    except:
        print("请求失败")
        return (None, None)
    soup = BeautifulSoup(keywordResponse.text, utils.htmlParser)
    htmlText = keywordResponse.text
    return (soup, htmlText)

# 对搜索出来的页面进行操作
def searchAction(soup, path):

    pageListCount = getSearchOnePageListCount(soup)
    print("当前页面有 {} 个资源".format(pageListCount))

    # 获取所有资源子链接的url
    urlList = []
    for index in range(1, pageListCount+1):
        urlInfo = soup.select(Formate.detailUrlSelectFormat(index))
        if(len(urlInfo) > 0):
            url = utils.baseURL + urlInfo[0].get("href") 
            #print(url)
            urlList.append(url)

    # 使用信号量控制并发的数量
    sem = Semaphore(value = 10)

    # 多线程处理上面的子链
    detailUrlThread = DetailUrlThread(urlList,sem,path)
    detailUrlThread.start()

    #等待接收
    detailUrlThread.join()

    return detailUrlThread.downloadInfos
  
# 获取此页资源数量
def getSearchOnePageListCount(soup) -> int:
    """ 每一页的列表的数量 """
    dataListInfos = soup.select("#data_list")
    if len(dataListInfos) == 0:
        return 0

    dataList = dataListInfos[0]
    dataText = dataList.get_text()
    # 判断资源为空不能通过dataList.contents来进行区别,以为数据为空的时候,这数组还是有值的而且大于0
    if "没有可显示资源" in dataText:
        return 0
    else:
        contents= dataList.contents
        del contents[0]
        count = int(len(contents) / 2)
        return count




class DetailUrlProduce():
    """ 详细网址抓取器 """

    def __init__(self, soup, pageListCount, htmlText):
        """ DetailUrlProduce的初始化方法 """
        super().__init__()
        self.soup = soup
        self.pageListCount = pageListCount
        self.htmlText = htmlText

    def getAllDetailUrls(self) -> list:
        """ 获取所有的详细页面的Url 返回一个url数组 """
        print("一页的数量{}".format(self.pageListCount))
        detailUrls = []
        for index in range(1, self.pageListCount + 1):
            someUrlsInfo = self.soup.select(Formate.detailUrlSelectFormat(index))
            if len(someUrlsInfo) > 0:
                detailUrl = utils.baseURL + someUrlsInfo[0].get("href")
                print(detailUrl)
                detailUrls.append(detailUrl)
                #self.getListInfo(index = index)
            else:
                continue
        return detailUrls

    def getListInfo(self, index):
        """ 获取列表一行里的基本信息 """
        selector = etree.HTML(self.htmlText)
        size = selector.xpath(Formate.listSizeSelectFormat(index))[0].text
        makeSeedNum = selector.xpath(Formate.listMakeSeedNumSelectFormat(index))
        downloading = selector.xpath(Formate.listDownloadingSelectFormat(index))
        finished = selector.xpath(Formate.listFinishedSelectFormat(index))
        push = selector.xpath(Formate.listPushSelectFormat(index))[0].text
        print(size, makeSeedNum, downloading, finished, push)