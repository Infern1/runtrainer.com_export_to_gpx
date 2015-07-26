# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from runtrainer.items import RuntrainerItem

from itertools import izip

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

class LoginSpider(scrapy.Spider):
    name = 'runtrainer'
    allowed_domains = ['runtrainer.com']
    start_urls = ['http://runtrainer.com/login.php']

    def __init__(self, user='',password='', *args, **kwargs):
        super(LoginSpider, self).__init__(*args, **kwargs)
        self.user = user
        self.password = password
        
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': self.user, 'password': self.password},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "password is invalid" in response.body:
            self.logger.error("Login failed")
            return
        else:
            #print "I'm in"
            #return
            yield scrapy.Request('http://runtrainer.com/mystats.php', self.parse_2)
            

    def parse_2(self, response):
        
        #get all links
        links = response.xpath('//a[contains(@class, "glyphicon-eye-open")]/@href').extract () # 
        for link in links:
            activity_url = "http://runtrainer.com/mystats.php" + link
            yield scrapy.Request(activity_url,self.parse_3)
            #print "link is %s" % activity_url

    def parse_3(self, response):
        items = []
        item = RuntrainerItem()
       
        item ["distance"] = response.xpath('//html/body/div[1]/div[2]/div[3]/div[1]/h2/text()').extract()[0].strip() 
        item ["time"]     = response.xpath('//html/body/div[1]/div[2]/div[3]/div[2]/h2/text()').extract()[0].strip() 
        item ["date"]     = response.xpath("//a[@class='mystatscurrent']/text()").extract()[0].strip()
        item ["avg"]      = response.xpath('//html/body/div[1]/div[2]/div[3]/div[3]/h2/text()').extract()[0].strip() 
        item ["cal"]      = response.xpath('//html/body/div[1]/div[2]/div[3]/div[4]/h2/text()').extract()[0].strip() 
        li                = response.xpath('//script')[1].re(r'new google\.maps\.LatLng\(([0-9.]+), ([0-9.]+)\)')

        #remove last six elements since they contain zoomlevel, start and end point
        li = li[:-6]
        lat_ar = []
        lng_ar = []
        for lat, lng in pairwise(li):        
            lat_ar.append(lat)
            lng_ar.append(lng)
            #print "lat %s lng %s " % (lat, lng)
        
        item ["Lat"] = lat_ar
        item ["Lng"] = lng_ar
        items.append(item)
        return items


