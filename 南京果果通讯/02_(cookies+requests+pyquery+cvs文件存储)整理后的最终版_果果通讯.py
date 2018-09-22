# -*- coding: utf-8 -*-
# @Time    : 2018-08-11 9:41
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 02_(pyquery+cvs文件存储)整理后的最终版_果果通讯.py
# @Software: PyCharm

# 引用requests中的cookies中的库和函数
import csv

import requests
from pyquery import PyQuery as pq

jar = requests.cookies.RequestsCookieJar()
cookie = jar.set('JSESSIONID', '37395F7616EDEC8B994A0963D439B1C5')

# 模拟浏览器来设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',

}

# 利用请求头和cookies来有权限获取url的源码
r = requests.get('http://www.njggtx.com/quoteList.action?gsdm=39773&km=&pp=%E5%B0%8F%E7%B1%B3&network=&tykhgsdm=',
                 cookies=jar,
                 headers=headers)
# print(r.text)

# 把获取的网页源码保存到本地
with open('njggtx.html', 'w', encoding='gbk') as file:
    file.write(r.text)

# 用pyquery方法来解析
doc = pq(filename='njggtx.html')
content = doc('#dataTable').text()
# print(content)

# 　数据处理，以换行做切片成一个列表存储起来
list_content = content.split('\n')

# 删除无用的数据
del list_content[0]

# print(list_content)
# 对列表进行格式化成一个如 [1,2,3,...100]变成 [[1,2,3],[4,5,6]....]
result = [list_content[i:i + 4] for i in range(0, len(list_content), 4)]

# 文件的写入---csv文件存储
with open('result.csv', 'w') as file:
    writer = csv.writer(file)
    # 写入头
    writer.writerow(['手机型号', '价格', '详细信息', '加入购物车'])
    # 循环写入读取的数据
    for i in result:
        writer.writerow(i)
