# -*- coding: utf-8 -*-
# @Time    : 2018-08-13 8:51
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : test.py
# @Software: PyCharm
from pyquery import PyQuery as pq
import requests


html_code = requests.get('http://news.sina.com.cn/c/2018-08-13/doc-ihhqtawx6755550.shtml').content.decode('utf-8')
print(html_code)
# 用pyquery来解析文章的内容和发布时间
# doc = pq(html_code)
# time = doc('.date').text()
# content = doc('#article').text()
# # return time, content
# # 测试
# print(time, content)