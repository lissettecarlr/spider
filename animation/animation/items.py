# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#需要抓取的项目
#AnimeName 动漫的标题
#AnimeEpisode 动漫的集数
#AnimeMagnet 动漫的下载链接
class AnimationItem(scrapy.Item):
    AnimeName = scrapy.Field()
    AnimeEpisode = scrapy.Field()
    AnimeMagnet = scrapy.Field()

