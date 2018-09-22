# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem


class TextPipeline(object):
    def __init__(self):
        # 如果长度超过50就分段处理
        self.limit = 50

    # 主要用于对item数据的处理有时候可能不需要的数据进行处理再存储
    def process_item(self, item, spider):
        # 如果有内容则对内容进行操作

        if item['text']:
            # 如果长度大于设置的最大值则对多余的部分进行截取并把多余的部分用省略号来代替

            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
                # 再把所有的数据进行返回
                return item
            # return item

        else:
            # 如果没有则抛出异常处理的消息
            return DropItem('Missing Text')


class MongoPipeline(object):
    '''MongoDB数据存储管道'''

    def __init__(self, mongo_url, mongo_db):
        # 传入两个参数
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 从settings里拿到需要的两个常量
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        # 开始之前启动这个操作
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # 数据库的插入操作
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        # 关闭数据库
        self.client.close()



