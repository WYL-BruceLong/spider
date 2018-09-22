# -*- coding: utf-8 -*-
# @Time    : 2018-08-12 20:14
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_新浪新闻的爬取_正则+urllib.py
# @Software: PyCharm
import re
from urllib.request import *
from pyquery import PyQuery as pq

import requests


def get_url_list(url):
    """
    根据url来获取子网页中的url地址和新闻的标题
    :param url: 主网页的url
    :return: url_list and news_title
    """
    # 请求头（伪装浏览器）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    # 用来添加报头信息
    opener = build_opener()

    # 把请求头里的伪装浏览器添加到报头里
    opener.add_handler = [headers]
    data = opener.open(url).read()
    html_data = data.decode('utf-8', 'ignore')

    # 正则表达式（子新闻的url和新闻的标题）
    pat = '<a target="_blank" href="(http://news.sina.com.cn/.*?)".*?>(.*?)</a>'

    url_list = re.compile(pat, re.S).findall(html_data)
    del url_list[0]
    return url_list


def get_secondnews_content(news_url):
    """
    获取子网页的发布时间和内容
    :param news_url: 新闻的url
    :return: 新闻的发布时间和内容
    """

    html_code = requests.get(news_url).content
    # 用pyquery来解析文章的内容和发布时间
    doc = pq(html_code)
    time = doc('.date').text()
    content = doc('#article').text()
    return time, content
    # 测试
    # print(time.encode('utf-8'), content)


def save_data(news_title, news_contnet):
    """
    新闻的存储
    :param news_title: 新闻的标题
    :param news_contnet: 新闻的内容（新闻发布时间，新闻的正文）
    :return:
    """
    # 文件保存的路径
    file_path = './sina_news/' + news_title + '.txt'
    # 文件的操作
    with open(file_path, 'w', encoding='utf-8') as f:
        # 写入
        f.write(str(news_title) + '\n\n' + str(news_contnet[0]) + '\n' + str(news_contnet[1]))


def main():
    """主程序-新浪新闻文章的下载"""

    # 初始化url
    url = 'https://www.sina.com.cn/'
    # 从主页得到新闻子网页中的url和title
    url_list = get_url_list(url)

    # 根据得到的url遍历分离url和title
    for news_url, news_title in url_list:
        # print(news_title, news_url)
        # 考虑到文件名
        news_title = re.sub('[|/*?<>:]', '.', news_title)
        news_contnet = get_secondnews_content(news_url)
        # 文件的存储
        save_data(news_title, news_contnet)


if __name__ == '__main__':
    main()
