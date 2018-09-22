# -*- coding: utf-8 -*-
# @Time    : 2018-08-14 8:04
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_淘宝商品图片大图的爬取.py
# @Software: PyCharm
import re
import sys
import time

import gevent
from gevent import monkey
# sys.setrecursionlimit(1000000)
# 请猴子打补丁
monkey.patch_all()
import requests


def get_img_url_list(url):
    """根据传过来的url来解析所需要图片的下载链接"""

    # 1.先伪装浏览器
    headers = {
        'Cookie':' UM_distinctid=1650e48146cd10-0f146d4cc671f4-47e1039-100200-1650e48146ec5c; Hm_lvt_3ef185224776ec2561c9f7066ead4f24=1533802803,1533859967,1533999198,1534247172; CNZZDATA1253486800=584187938-1533540490-%7C1534243027; Hm_lpvt_3ef185224776ec2561c9f7066ead4f24=1534247186',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # 2.用requests库来得到网页的源码
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    print(response.text)
    # 3.对得到的源码进行解析处理,可以用正则，xpath，beautifulsoup或pyquery
    pat = '(//g-search3.alicdn.com/img/bao/uploaded/i4/.*?.jpg)'
    img_url_list = re.compile(pat).findall(str(response.text))
    # print(img_url_list)
    # print(len(img_url_list))
    print('\n\n此页面图片已经全部拿到……等待下载……')
    return img_url_list


def down_img(img_path, new_img_url):
    """图片文件的下载"""
    print('\n图片正在下载……')
    # 用requests获取图片文件的二进制数据
    img_data = requests.get(new_img_url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)

    print('\n图片下载成功……@_@……')
    # time.sleep(.1)


def main():
    """淘宝商品图片大图的爬取-主程序"""
    # 需要爬取商品的内容
    name = '连衣裙'

    # 创建一个gevent_list列表


    # 需要爬取数据的页面
    for i in range(10):
        page_num = i * 60

        url = 'https://s.taobao.com/list?spm=a21bo.2017.201867-links-0.4.5af911d98e1INj&q=%s&cat=16&seller_type=taobao&oetag=6745&source=qiangdiao&bcoffset=12&s=%s' % (name, str(page_num))
        # 通过程序来获取图片的url
        img_url_list = get_img_url_list(url)

        # 循环遍历url_list得到一个下载图片的img_url
        for img_url in img_url_list:
            print(img_url)

            # 保存图片的路径和图片的名字
            img_path = './images/' + img_url[-13::1]

            # 图片的url在之前加http:
            new_img_url = 'http:' + img_url
            down_img(img_path, new_img_url)
            # 把任务添加到协程里


        print('\n\n第%s页：已经下载完成' % str(i))
        # time.sleep(.5)
    print('\n\n\n所有图片下载成功……')



if __name__ == '__main__':
    gevent_list = list()
    spawn = gevent.spawn(main)
    gevent_list.append(spawn)
    gevent.joinall(gevent_list)
