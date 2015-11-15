# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import MySQLdb
from scrapy.http import Request
from scrapy.exceptions import DropItem


class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='user', 'passwd', 'dbname', 'host', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()


def process_item(self, item, spider):
    try:
        self.cursor.execute("""INSERT INTO db_name (company_name, company_logo, job_title, job_date, job_location, job_experience, job_function, employment_type, industry, job_description, apply_link, company_description, company_youtube_video)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (item['company_name'].encode('utf-8'),
                        item['company_logo'].encode('utf-8'),
                        item['job_title'].encode('utf-8'),
                        item['job_date'].encode('utf-8'),
                        item['job_location'].encode('utf-8'),
                        item['job_experience'].encode('utf-8'),
                        item['job_function'].encode('utf-8'),
                        item['employment_type'].encode('utf-8'),
                        item['industry'].encode('utf-8'),
                        item['job_description'].encode('utf-8'),
                        item['apply_link'].encode('utf-8'),
                        item['company_description'].encode('utf-8'),
                        item['company_youtube_video'].encode('utf-8')))

        self.conn.commit()

    except MySQLdb.Error:
        pass

    return item
