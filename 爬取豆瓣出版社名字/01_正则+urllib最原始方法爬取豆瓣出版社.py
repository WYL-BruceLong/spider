# -*- coding: utf-8 -*-
# @Time    : 2018-08-12 15:07
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_正则+urllib最原始方法爬取豆瓣出版社.py
# @Software: PyCharm
import csv
import re
import requests

# 定义一个url地址

url = 'https://read.douban.com/provider/all'
# url__read_data = urlopen(url).read()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}
response = requests.get(url, headers=headers)

# print(response.text)
# 获取到的html源码
html = response.text

# 正则匹配
pat = '<div class="name">(.*?)</div>'
result = re.compile(pat).findall(html)

# print(result)
# 在本地新建一个文件用来存储数据
# with open('./出版社.txt', 'w', encoding='utf-8') as f:
with open('./出版社.csv', 'w') as f:
    for i, book_name in enumerate(result):
        # print(i, book_name)   # 测试
        # 把数据保存到txt文件中
        # f.write("%d\t%s\n" % (i, book_name))
        # 把数据保存在csv格式里
        writer = csv.writer(f)
        writer.writerow([i, book_name])
