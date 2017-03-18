# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class MongoPipeline(object):

    collection_name = 'coll_reports_html'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 按url为唯一的key，避免重复插入
        cursor = self.db[self.collection_name].find({"url": dict(item)["url"]})
        count = 0
        for item in cursor:
            count += 1
        if count == 0:
            self.db[self.collection_name].insert(dict(item))

        return item


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class ScrapyReportsHtmlPipeline(object):
    def process_item(self, item, spider):
        return item
