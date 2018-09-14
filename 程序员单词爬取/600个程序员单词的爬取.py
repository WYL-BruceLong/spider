# -*- coding: utf-8 -*-
# @Time    : 2018-08-25 17:35
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 600个程序员单词的爬取.py
# @Software: PyCharm
import json
from pyquery import PyQuery as pq

import requests


# 利用爬虫来获取关于程序员的600个单词

def get_web_page():
    '''
    分析网页，得到结果是一个js渲染的网页，利用requests来把js中的真正的url传递
    过来，利用字符串的操作来得到一个真正的json数据
    :return: html源码
    '''
    # 从网上找的一个url地址
    url = 'https://query.yahooapis.com/v1/public/yql?q=use%20%22https%3A%2F%2Fraw.githubusercontent.com%2Fyql%2Fyql-tables%2Fmaster%2Fdata%2Fdata.headers.xml%22%20as%20headers%3B%20select%20*%20from%20headers%20where%20url%3D%22https%3A%2F%2Fraw.githubusercontent.com%2FGeorgewgf%2Frecitewords%2Fmaster%2Findex.html%22&format=json&diagnostics=true&callback=HTMLPreview.loadHTML'
    # 页面分析得到源码
    res = requests.get(url)
    json_loads = json.loads(res.text.lstrip('/**/HTMLPreview.loadHTML(').rstrip(');'))

    html = json_loads['query']['results']['resources']['content']
    # print(html)
    return html


def parse_web_page(html):
    '''
    根据传递过来的网页源码来通过pyquery模块来得到需要的数据
    :param html: 网页的源码
    :return: 所需要的内容，单词和翻译
    '''

    # 把网页源码放到pyquery解析器中
    doc = pq(html)
    # 根据class为wordItemBox的来筛选需要的内容块并得到一个生成器来为了方便下面数据的遍历
    contents = doc('.wordItemBox').items()
    return contents


def main():
    '''利用爬虫来获取关于程序员的600个单词'''

    # 得到的网页源码
    html = get_web_page()

    # 解析网页得到需要的数据
    contents = parse_web_page(html)

    # 打印需要的数据
    # 把需要的数据遍历并得到真正的内容
    for i, temp in enumerate(contents):
        word = temp('.word').text()
        translate = temp('.translate').text()
        print(i, word, translate)


if __name__ == '__main__':
    main()
