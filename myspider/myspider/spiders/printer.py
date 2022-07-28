import scrapy
from myspider.items import MyspiderItem

class PrinterSpider(scrapy.Spider):
    name = 'printer'
    #allowed_domains = ['test']
    start_urls = ['http://172.19.180.249']

    def parse(self, response):
        item = MyspiderItem()
        status = response.xpath("//span[@class='status-message']/text()").extract()
        if(status != []):
            s = status[0]
            s = s.replace('\n', '')
            s = s.replace('\r', '')
            s = s.replace(' ', '')
            print(s)
            item['printerStatus'] = s
            yield item
        return s
