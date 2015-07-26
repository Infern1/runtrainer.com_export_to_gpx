# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RuntrainerItem(scrapy.Item):

    distance = scrapy.Field()
    date     = scrapy.Field()
    time     = scrapy.Field()
    avg      = scrapy.Field()
    cal      = scrapy.Field()
    Lat      = scrapy.Field()
    Lng      = scrapy.Field()


