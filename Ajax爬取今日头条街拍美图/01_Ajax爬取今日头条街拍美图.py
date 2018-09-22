# -*- coding: utf-8 -*-
# @Time    : 2018-08-15 10:27
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_Ajax爬取今日头条街拍美图.py
# @Software: PyCharm
import os
from hashlib import md5
from multiprocessing.pool import Pool
from urllib import request
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
    # 添加的请求头
    headers = {
        'referer': 'https',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    # 把参数组用urlencode进行编码并加入到要访问的url里面
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    # 异常处理
    try:
        # 用requests库来解析url得到的数据
        response = requests.get(url, headers=headers)
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

    if json.get('data'):
        # json>data>下一个目录
        try:
            for item in json.get('data'):
                title = item.get('title')
                images = item.get('image_list')
                for image in images:
                    yield {
                        'image': image.get('url'),
                        'title': title
                    }
        except Exception as e:
            print("Error:", e)
            return None


def save_image(item):
    '''
    实现一个保存图片的方法，在该方法中，首先根据item的title来创建文件夹，然后请求这个图片链接，获取图片的二进制数据，以二进制的形式写入文件。图片的名称可以使用其内容的MD5值，这样可以去除重复
    :param item: item就是前面get_images()方法返回的一个字典
    :return:
    '''

    # 判断是否有以标题为名的文件夹，如果没有则利用os模块新建一个文件夹
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
        try:
            # 请求能够根据图片的下载url来得到相应的二进制数据
            response = requests.get(item.get('image'))
            # 请求成功后的数据处理
            if response.status_code == 200:
                # 创建一个文件的保存路径，用数组的方式来接收数据
                file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
                # 判断这个文件的路径是否存在，不存在则新建一个文件，并把得到的二进制数据写入到文件里面
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print('Image wrote success')
                else:
                    print('Already Downloaded', file_path)
        except requests.ConnectionError:
            print("Failed to save Image")


def write_img(file_name, image_url):
    """读取图片内容"""
    # 读取所有图片
    # req = request.urlopen(image_url)
    # content = req.read()

    send_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
    }

    # 发送请求 第一个是请求的地址,第二个请求的头,第三个是请求的方式
    req = request.Request(url= 'http:'+image_url, headers=send_headers, method="GET")

    response = request.urlopen(req)
    content = response.read()

    # 写到文件中
    with open("./images/%s.jpg" % file_name, 'wb') as f:
        f.write(content)


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
        # print(item)
        # save_image(item)
        write_img(item['title'],item['image'])



# 起始位置初始化
GROUP_START = 1
GROUP_END = 20
if __name__ == '__main__':
    # 传递数据参数，并利用多进程的线程池，调用其map()方法实现多进程下载
    # groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    # main(20)
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
