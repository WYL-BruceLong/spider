# -*- coding: utf-8 -*-
# @Time    : 2018-08-11 19:47
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_正则来批量获取美女图片.py
# @Software: PyCharm
import re
from urllib.request import *
import requests
import gevent
from gevent import monkey

# 打补丁
monkey.patch_all()


def get_source_code(url):
    """
根据给的url来获取html源码
    :param url:url地址
    :return: none
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # return response.text
        print(response.text)
    return None


def get_img_src(html_code):
    """
用正则来匹配内容，得到一个图片中的src的列表
    :param code: 传入一个网页的源码进行分析
    :return:
    """
    # print(html_code)
    # 正则使用方法首在哪一个容器下面，其次就是找不同参数相同的值 用非贪婪的方法来找需要的数据
    # 此处用的格式:.*?相同的class或者id.*?>(.*?这里就是所需要的内容)以怎么结尾</i标签名>
    pattern = re.compile(
        '<img.*?data-original="(.*?)".*?>',
        re.S
    )
    # 把产生的对象放到一个正则方法里findall（）方法是指匹配正则表达式的所有内容match()是用来手动写以字符串开始或结束
    # search()是指从开头扫描直到遇到第一个满足条件的就返回（不是全部哦）
    img_url_list = re.findall(pattern, html_code)
    return img_url_list


def download_img(img_url, img_name):
    """
下载一张图片
    :param img_url: 获取一张图片的url
    :param img_name: 给图片的一个名字
    :return:
    """
    print("美女在路上:", img_name)
    # 打开对应图片的地址
    # request请求,response响应
    response = urlopen(img_url)
    # 读取图片的内容
    content = response.read()
    # 保存 图片
    with open(img_name, 'wb') as f:
        f.write(content)

    print("欢迎美女的到来:", img_name)


def main():
    """主程序，斗鱼美图批量下载器"""
    # 定义一个url
    url = 'https://www.douyu.com/g_yz'

    # 得到源码函数
    html_code = get_source_code(url)

    # 拿到每张图片的网址，并以列表的形式返回
    # img_url_list = get_img_src(html_code)
    # print(img_url_list)

    # 图片下载
    # 给图片起名
    image_num = 1

    # 创建一个gevent列表
    gevent_list = list()

    # 循环遍历每张图片
    # for img_url in img_url_list:
    #     # 下载一张图片，并保存下来
    #     save_path = "./images/%d.jpg" % image_num
    #     # download_img(img_url, save_path)
    #     # 开启一个协程
    #     spawn = gevent.spawn(download_img, img_url, save_path)
    #
    #     image_num += 1
    #     gevent_list.append(spawn)
    #
    # gevent.joinall(gevent_list)

if __name__ == '__main__':
    main()
