# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class MyspiderPipeline:
    
    def __init__(self):
        self.file = open('printerStatus.jl', 'a')
        self.lastPrinterStatus = ""

    def process_item(self, item, spider):
        if(item['printerStatus'] != self.lastPrinterStatus):
            self.lastPrinterStatus = item['printerStatus']
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        return item

    def open_spider(self,spider):
        print("open spider")

    def close_spider(self,spider):
        print("close spider")
