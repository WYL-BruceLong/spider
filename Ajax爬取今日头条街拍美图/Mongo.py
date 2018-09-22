# -*- coding: utf-8 -*-
# @Time    : 2018-09-01 19:49
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : config.py
# @Software: PyCharm
import pymongo

# 定义一个数据的连接
MONGO_URL = 'localhost'
# 初始化一个数据的名称
MONGO_DB = 'toutiao'
# 初始化一个数据的表名
MONGO_TABLE = 'toutiao'


class Mongo(object):
    def __init__(self, database, table,result):
        '''初始化'''
        # 创建一个客户端对象
        self.client = pymongo.MongoClient(MONGO_URL)
        # 用客户端来创建一个数据的名称
        self.db = client[MONGO_DB]

    def save_to_mongo(self,result):
        '''
        把数据存储到mongodb数据库中
        :param result: 传入需要保存的数据
        :return: 如果保存成功就返回true否则返回false
        '''

        # 把数据插入到一个表中
        if db[MONGO_TABLE].insert(result):
            print('存储到MongoDB成功', result)
            return True
        return False
