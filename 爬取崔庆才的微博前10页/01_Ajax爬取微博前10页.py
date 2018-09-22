# -*- coding: utf-8 -*-
# @Time    : 2018-08-14 21:34
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_Ajax爬取微博前10页.py
# @Software: PyCharm

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

# 需要请求的网址
base_url = 'https://m.weibo.cn/api/container/getIndex?'
# 添加的请求头
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 数据的处理
# 创建一个数据库对象
client = MongoClient()
# 指定数据库
db = client['weibo']
# 指定集合
collection = db['weibo']


# 得到网页的数据
def get_page(page):
    # 参数组
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    # 组成新的url
    url = base_url + urlencode(params)
    # 异常处理
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # 如果访问成功则返回的是一个json数据
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


# 解析网页
def parse_page(json):
    if json:
        # 通过get的方式来获取cards中的数据，在cards中是一个列表
        # [{card_type: 9, itemid: "1076032830678474_-_4268541799176271",…},…]
        items = json.get('data').get('cards')
        # 循环遍历得到一篇文章内的所有数据
        for item in items:
            try:
                # 从items中得到一个mblog的字段
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id', 2)
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count', 3)
                weibo['comments'] = item.get('comments_count', 5)
                weibo['reposts'] = item.get('reposts_count', 6)
                yield weibo
            except Exception as e:
                print('Error', e)


# 数据存储-Mongodb来存放数据
def save_to_mongo(result):
    collection_insert = collection.insert(result)
    if collection_insert:
        print('Saved to Mongo!success')
        print(collection_insert)


if __name__ == '__main__':

    # 循环得到前10页的内容
    for page in range(1, 11):
        # 把数据传给get_page
        json = get_page(page)
        # 把得到的json数据给解析网页的parse_page函数
        results = parse_page(json)
        # 循环输入每一页的内容
        for result in results:
            print(result)
            # 数据存储
            save_to_mongo(result)

    # 把数据传给get_page
    # json = get_page(1)
    # # 把得到的json数据给解析网页的parse_page函数
    # results = parse_page(json)
    # # 循环输入每一页的内容
    # for result in results:
    #     print(result)
