# -*- coding: utf-8 -*-
# @Time    : 2018-08-14 19:57
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : test.py
# @Software: PyCharm
import requests

url = 'https://s.taobao.com/list?spm=a21bo.2017.201867-links-0.4.5af911d9bcCTjk&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&cat=16&seller_type=taobao&oetag=6745&source=qiangdiao'
response = requests.get(url)
response.encoding = 'utf-8'
with open('./text.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
