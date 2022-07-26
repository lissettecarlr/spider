# spider


## 框架Scrapy
安装

```
pip install Scrapy
```

依赖
```
apt install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
```

目录结构：
* scrapy.cfg: 项目的配置文件。
* mySpider/: 项目的Python模块，将会从这里引用代码。
* mySpider/items.py: 项目的目标文件。
* mySpider/pipelines.py: 项目的管道文件。
* mySpider/settings.py: 项目的设置文件。
* mySpider/spiders/: 存储爬虫代码目录。