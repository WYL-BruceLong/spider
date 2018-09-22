# -*- coding: utf-8 -*-
# @Time    : 2018-09-01 10:37
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : demo.py
# @Software: PyCharm
import json
import re

import requests

url = 'http://toutiao.com/group/6595715557318722051/'

# 添加的请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

response = requests.get(url, headers=headers)
# print(response.text)

pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
result = re.search(pattern, response.text)

# print(result.group(1))
d = re.sub('\\\\', '', result.group(1))
# print(d)
data = json.loads(d)
for temp in data['sub_images']:
    print(temp['url'])
