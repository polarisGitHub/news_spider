# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from news_spider import store


class NewsSpiderPipeline(object):

    def __init__(self):
        self.db = store.DBHelper()

    def process_item(self, item, spider):
        self.db.insert(item)
        return item
