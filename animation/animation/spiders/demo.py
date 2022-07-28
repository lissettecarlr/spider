import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    #allowed_domains = ['test']
    start_urls = ['http://172.19.180.249/']

    def parse(self, response):
        print(response.text)
      
