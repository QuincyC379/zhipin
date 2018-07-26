# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from pymongo import MongoClient

from zhipin.config import *


class ZhipinPipeline(object):
    def __init__(self):
        self.f = open('job_info.json', 'w', encoding='utf-8')
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]

    def save_to_mongo(self, content):

        if self.db[MONGO_TABLE].insert(content):
            print('成功保存到mongoDB', content)
    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(text + '\n')
        self.save_to_mongo(dict(item))
        return item

    def close_spider(self, spider):
        self.f.close()
