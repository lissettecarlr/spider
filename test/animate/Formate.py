""" 一些简单的格式化函数 """

# page格式化
def pageFormate(pageNum = None) -> str:
    return "&page={}".format(pageNum or 1)

# 搜索格式化
def keywordFormat(keyword) -> str:
    return "/search.php?keyword=" + keyword

# 详细url的copy-selector格式化
def detailUrlSelectFormat(index) -> str:
    return "#data_list > tr:nth-child({}) > td:nth-child(3) > a".format(index)

""" 下面是想通过搜索列表获取其文件大小 种子数量 正在下载 完成 发布者 通过lxml框架进行 """

# 列表的单个文件大小
def listSizeSelectFormat(index) -> str:
    return '//*[@id="data_list"]/tr[{}]/td[4]'.format(index)

# 列表的做种梳理 有问题
def listMakeSeedNumSelectFormat(index) -> str:
    return '//*[@id="data_list"]/tr[{}]/td[5]/span/text'.format(index)

# 列表下载数量 有问题
def listDownloadingSelectFormat(index) -> str:
    return '//*[@id="data_list"]/tr[{}]/td[6]/span/text'.format(index)

# 列表完成的数量 有问题
def listFinishedSelectFormat(index) -> str:
    return '//*[@id="data_list"]/tr[{}]/td[7]/span/text'.format(index)

# 列表发布者
def listPushSelectFormat(index) -> str:
    return '//*[@id="data_list"]/tr[{}]/td[8]/a'.format(index)
