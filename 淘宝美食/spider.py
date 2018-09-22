# -*- coding: utf-8 -*-
# @Time    : 2018-09-01 21:23
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : spider.py
# @Software: PyCharm
import json
import re

import requests

# 在搜索框中输入美食得到的数据q=%E7%BE%8E%E9%A3%9F
url = 'https://s.taobao.com/search?q=%E7%BE%8E%E9%A3%9F'
response = requests.get(url)
print(response.text)

# 用正则对html源码进行解析到一个json数据
pattern = re.compile('g_page_config =(.*?});', re.S)
result = re.search(pattern, response.text)
# print(result.group(1))


try:
    # 发现并不是那么简单而是加密的数据并是有规律可寻的，以下是加密的几个数据段
    json_data = re.sub('(\\\\u003d)|(\\\\u0026)|(\\\\u003c)|(\\\\u003e)', '', result.group(1))
    print('数据解密成功')
    # print(json_data)
except Exception as e:
    print('数据解密失败，原因是：',e)


# json_dumps = json.dumps(json_data)
# print(json_dumps)
data_count = 1
data = json.loads(json_data)
# 分析json的数据并把需要的数据给读取出来
for good in data['mods']['itemlist']['data']['auctions']:
    print('商店名：{},商品标题:{},\n商品图片：{},\n商品产地：{},商品价格：{},付款人数：{},\n'.format(good['nick'], good['title'], good['pic_url'], good['item_loc'], good['view_price'],good['view_sales']))
    data_count += 1

print(data_count)
