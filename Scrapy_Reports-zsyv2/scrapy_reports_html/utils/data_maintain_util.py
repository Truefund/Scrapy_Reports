# -*- coding: utf-8 -*-

import scrapy_reports_html.settings
import pymongo


class DataMaintainUtil:

    def __init__(self):
        pass

    @classmethod
    def isUrlExist(cls, url):
        mongoUri = scrapy_reports_html.settings.MONGO_URI
        mongoDb = scrapy_reports_html.settings.MONGO_DATABASE
        mongoColl = scrapy_reports_html.settings.MONGO_COLLECTIOIN_REPORTS
        client = pymongo.MongoClient(mongoUri)
        db = client[mongoDb]

        count = db[mongoColl].find({"url": url}).count()
        if count == 0:
            return False
        return True
