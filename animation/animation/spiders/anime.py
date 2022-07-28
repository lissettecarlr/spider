import scrapy
import re

from animation.items import AnimationItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

#负责抓取网页数据的爬虫
class AnimeSpider(CrawlSpider):
  #爬虫名
	name = "anime"

  #允许抓取的域
	allowed_domains = ["dmnico.cn"]

  #初始抓取URL
	start_urls = [
		#"http://www.dmnico.cn/article/?aa3f8d5c14f17848ea25.html"
		"http://172.19.180.249/"
	]
  #抓取规则
	rules = (
		Rule(LinkExtractor(allow=(r'artttml/.*html')),callback='parse_item'),
	)

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, headers={"User-Agent": USER_AGENT})

  #解析抓取的数据
	def parse_item(self, response):
		# print(response.text)
		with open("TY.html", "w") as f:
			f.write(response.body)
		# item = AnimationItem()
		# item['AnimeName'] = re.split(r'\(|\[|\s', response.xpath(r'//title/text()').extract()[0])[0]
		# item['AnimeEpisode'] = response.selector.re(r'<a.*?magnet.*?>([\s\S]*?)<\/a>')
		# item['AnimeMagnet'] = response.selector.re(r'magnet:[?]xt=urn:btih:\w+')
		# if item['AnimeMagnet'] != []:
		# 	yield item
		# 	return item
