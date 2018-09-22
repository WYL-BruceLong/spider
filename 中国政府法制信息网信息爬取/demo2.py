# -*- coding: utf-8 -*-
# @Time    : 2018-08-30 11:11
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : demo.py
# @Software: PyCharm
import re

import requests

# post请求的参数
data = {
    'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '15', 'sourceContentType': '1', 'unitid': '1648',
    'webname': '中国政府法制信息网', 'permissiontype': '0'
}

# 请求的接口地址
url = 'http://www.chinalaw.gov.cn/module/web/jpage/dataproxy.jsp?perpage=15&startrecord=1'

# response = requests.post(url, data=data)
response = requests.post(url, data=data)
response.encoding = 'utf-8'
html = response.text
one_pate_url_list = re.findall('<a target="_blank" href="(/art/.*?\.html)">', html)
print(one_pate_url_list.pop())
print(one_pate_url_list)
print(len(one_pate_url_list))


