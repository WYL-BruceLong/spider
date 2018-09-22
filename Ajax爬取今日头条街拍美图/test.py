# -*- coding: utf-8 -*-
# @Time    : 2018-08-15 10:32
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : test.py
# @Software: PyCharm
from urllib.parse import urlencode

import requests


def get_page(offset):
    '''
    根据传的url+offset请求，来得到一个json的数据
    :param offset: 是一个可变的参数
    :return: 如果有数据则返回一个json数据，没有则返回None
    '''
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1'
    }

    # 把参数组用urlencode进行编码并加入到要访问的url里面
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    # 异常处理
    try:
        # 用requests库来解析url得到的数据
        response = requests.get(url)
        # 如果访问成功则返回一个json()的数据
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        # 如果访问失败则打印出原因并返回一个None
        print("Error:", e)
        return None

def get_images(json):
    '''从json数据中去查找有关图片的信息'''
    # 如查json里面有一个data的数据，则进行以下操作

    if json:
        # 通过get的方式来获取cards中的数据，在cards中是一个列表
        # [{card_type: 9, itemid: "1076032830678474_-_4268541799176271",…},…]
        items = json.get('data')
        # 循环遍历得到一篇文章内的所有数据
        for item in items:
            try:
                # 从items中得到一个mblog的字段
                for temp in range(20):
                    item_get = item.get(temp)
                    # 美拍
                    meipai = {}
                    meipai['title'] = item_get.get('title')
                    images = item_get.get('image_list')
                    for image in images:
                         meipai['image']= image.get('url')
                    print(meipai)
            except Exception as e:
                    print('Error', e)


def main(offset):
    """
    主程序-构造一个offset数组，遍历offset,提取图片链接，并将其下载
    :param offset:
    :return:
    """

    # 数据中转
    json = get_page(offset)
    # print(json)
    # print(get_images(json))
    for item in get_images(json):
        print(item)
        # save_image(item)


if __name__ == '__main__':
    main(20)