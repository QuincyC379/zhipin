# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhipinItem(scrapy.Item):
    # define the fields for your item here like:
    job_title = scrapy.Field()
    job_salary = scrapy.Field()
    job_company = scrapy.Field()
    company_size = scrapy.Field()
    publish_date = scrapy.Field()

