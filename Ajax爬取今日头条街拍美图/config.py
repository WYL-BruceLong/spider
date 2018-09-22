# -*- coding: utf-8 -*-
# @Time    : 2018-09-01 20:12
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : config.py
# @Software: PyCharm


# 定义一个数据的连接
import pymongo

MONGO_URL = 'localhost'
# 初始化一个数据的名称
MONGO_DB = 'toutiao'
# 初始化一个数据的表名
MONGO_TABLE = 'toutiao'

# 创建一个客户端对象
client = pymongo.MongoClient(MONGO_URL, connect=False)
# 用客户端来创建一个数据的名称
db = client[MONGO_DB]


def save_to_mongo(result):
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
