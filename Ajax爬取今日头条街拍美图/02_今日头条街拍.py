# -*- coding: utf-8 -*-
# @Time    : 2018-09-01 8:51
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 02_今日头条街拍.py
# @Software: PyCharm
import json
import re
from multiprocessing.pool import Pool

import requests
from bs4 import BeautifulSoup
from config import *
from requests import RequestException


def get_page_index(offset, keyword):
    '''得到一个页面的索引'''
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    # 请求方式一
    # url = 'https://www.toutiao.com/search_content/?'+urlencode(data)
    # response = requests.get(url)

    # 请求方式二
    url = 'https://www.toutiao.com/search_content/'
    try:
        response = requests.get(url, params=data)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page_index(html):
    '''解析json数据'''
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    '''得到详情页的数据'''
    # 添加的请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page_detail(html, url):
    '''解析详情页数据'''
    soup = BeautifulSoup(html, 'lxml')
    t = soup.select('title')
    for i in t:
        title = i.get_text()

    pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
    result = re.search(pattern, html)
    if result:

        # print(result.group(1))
        d = re.sub('\\\\', '', result.group(1))
        # print(d)
        data = json.loads(d)
        if data:
            images = [item.get('url') for item in data.get('sub_images')]
            for image in images:
                download_image(image, title)
            return {
                'title': title,
                'url': url,
                'images': images
            }
    else:
        None


def download_image(url, title):
    '''
    图片下载
    :param url: 下载的连接
    :return:
    '''
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            save_to_image(content, title)
        return None
    except RequestException:
        return None


count = 0


def save_to_image(content, title):
    global count
    '''
    保存图片文件
    :param content: 图片文件的内容
    :return:
    '''
    name = title + str(count)
    file_path = './头条/{}.{}'.format(name, 'jpg')
    with open(file_path, 'wb') as f:
        count += 1
        f.write(content)


def main(offset):
    '''主程序入口'''
    html = get_page_index(offset, '街拍')

    # print(html)
    for url in parse_page_index(html):

        if url:
            # print(url)
            html = get_page_detail(url)
            if html:
                # print(parse_page_detail(html, url))
                result = parse_page_detail(html, url)
                if result:
                    print(result)
                    # save_to_mongo(result)


GROUP_START = 1
GROUP_END = 20
if __name__ == '__main__':
    groups = [i * 20 for i in range(GROUP_START, GROUP_END)]
    pool = Pool()
    pool.map(main, groups)
