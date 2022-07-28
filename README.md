# spider


## 框架Scrapy

安装
python=3.7
```
pip install wheel
#进入pck中安装里面的两个包
pip install pywin32-303-cp37-cp37m-win_amd64.whl
pip install twisted_iocpsupport-1.0.2-cp37-cp37m-win_amd64.whl
pip install Scrapy
```

建立工程
```
scrapy startproject animation
```

建立个爬虫
```
scrapy genspider demo "test"
```

执行爬虫
```
scrapy crawl demo
```

将生产数据进行保存
```
scrapy crawl printer -o items.json
```

目录结构：
* scrapy.cfg: 项目的配置文件。
* mySpider/: 项目的Python模块，将会从这里引用代码。
* mySpider/items.py: 项目的目标文件。
* mySpider/pipelines.py: 项目的管道文件。
* mySpider/settings.py: 项目的设置文件。
* mySpider/spiders/: 存储爬虫代码目录。

XPath:
* /html/head/title: 选择HTML文档中 <head> 标签内的 <title> 元素
* /html/head/title/text(): 选择上面提到的 <title> 元素的文字
* //td: 选择所有的 <td> 元素
* //div[@class="mine"]: 选择所有具有 class="mine" 属性的 div 元素