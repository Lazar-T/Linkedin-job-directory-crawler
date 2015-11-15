# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinCrawlerItem(scrapy.Item):
    #page_url = scrapy.Field()
    company_logo = scrapy.Field()
    company_name = scrapy.Field()
    job_title = scrapy.Field()
    job_date = scrapy.Field()
    job_location = scrapy.Field()
    job_experience = scrapy.Field()
    job_function = scrapy.Field()
    employment_type = scrapy.Field()
    industry = scrapy.Field()
    job_description = scrapy.Field()
    apply_link = scrapy.Field()
    company_description = scrapy.Field()
    company_youtube_video = scrapy.Field()
