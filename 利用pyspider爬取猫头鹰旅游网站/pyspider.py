#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-09-04 19:22:25
# Project: Demo

from pyspider.libs.base_handler import *
import re
import pymongo


class Handler(BaseHandler):
    crawl_config = {
    }
    # 保存到MongoDB
    MONGO_URL = 'localhost'
    MONGO_DB = 'trip'
    MONGO_COLLECTION = 'London'
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Attractions-g186338-Activities-London_England.html',
                   callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.listing_title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)

        next = response.doc('div.al_border.deckTools.btm > div > div > a').attr.href
        self.crawl(next, callback=self.index_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        name = response.doc('#HEADING').text()
        rating = response.doc('div.ratingContainer > a > span').text().rstrip('\xa0条点评')
        address = response.doc('div.detail_section.address > span > span:nth-child(2)').text()
        name = re.sub('\n', '', name)
        phone = response.doc('div.contactType.phone > div').text()
        duration = response.doc('#component_3 > div > div:nth-child(4) > div').text().lstrip('建议时间：')
        return {
            'url': response.url,
            "name": name,
            "rating": rating,
            "address": address,
            "phone": phone,
            "duration": duration,
        }

    def on_result(self, result):
        if result:
            self.save_to_mongo(result)

    def save_to_mongo(self, result):
        '''
        保存到MongDB
        :param result:结果
        :return:
        '''
        try:
            if self.db[self.MONGO_COLLECTION].insert(result):
                print('存储到MongoDB成功')
        except Exception as e:
            print('存储到MongoDB失败，原因是：', e)