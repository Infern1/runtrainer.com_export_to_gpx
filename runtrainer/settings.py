# -*- coding: utf-8 -*-

# Scrapy settings for runkeeper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'runtrainer'

SPIDER_MODULES = ['runtrainer.spiders']
NEWSPIDER_MODULE = 'runtrainer.spiders'

ITEM_PIPELINES = {
    'runtrainer.pipelines.GpxFileOutput': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'runtrainer (+http://www.yourdomain.com)'
