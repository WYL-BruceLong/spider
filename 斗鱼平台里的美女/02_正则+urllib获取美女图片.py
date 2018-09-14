# -*- coding: utf-8 -*-
# @Time    : 2018-08-13 9:31
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 02_正则+urllib获取美女图片.py
# @Software: PyCharm
import re
from urllib.request import *
import gevent
from gevent import monkey

# 请猴子打补丁
monkey.patch_all()


def get_url_list(url):
    """
    根据url来获取子网页中的url地址
    :param url: 主网页的url
    :return: url_list
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
    # print(html_data)

    # 正则表达式（子新闻的url和新闻的标题）
    pat = '<img alt="(.*?)" data-original="(.*?)".*? class="JS_listthumb".*?>'

    url_list = re.compile(pat, re.S).findall(html_data)
    return url_list
    # print(url_list)


def download_img(i, title, dy_url):
    """
    图片下载
    :param title: 图片的名字
    :param dy_url: 图片的下载地址
    :return: 
    """
    file_path = './dy_img/' + title + '.jpg'
    print('第%s张' % str(i) + '正在加载：%s' % file_path)

    response = urlopen(dy_url)
    with open(file_path, 'wb') as f:
        # 循环读取数据
        while True:
            data = response.read(1024)
            # 判断是否有数据
            if data:
                f.write(data)
            else:
                break
    print('加载成功' + '@_@' + '*' * 10 + '@_@')


def main():
    """主程序-斗鱼美女下载器"""
    url = 'https://www.douyu.com/g_yz'
    url_list = get_url_list(url)

    # 数据处理
    num = 1
    # 定义一个geventlist
    gevent_list = list()
    for title, dy_url in url_list:
        # 文件写入-下载图片
        # download_img(num, title, dy_url)
        # 开启一个协程
        spawn = gevent.spawn(download_img, num, title, dy_url)
        # 把协添加到等待列表中
        gevent_list.append(spawn)
        num += 1
    # 主线程等待所有的协程执行完成以后程序再退出
    gevent.joinall(gevent_list)
    print('\n\n\n美女文件全部加载成功@_@……')


if __name__ == '__main__':
    main()
