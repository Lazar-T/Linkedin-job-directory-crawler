# -*- coding: utf-8 -*-

# Scrapy settings for linkedin_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'linkedin_crawler'

SPIDER_MODULES = ['linkedin_crawler.spiders']
NEWSPIDER_MODULE = 'linkedin_crawler.spiders'

ITEM_PIPELINES = {'linkedin_crawler.pipelines.MySQLStorePipeline': 300}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'linkedin_crawler (+http://www.yourdomain.com)'
