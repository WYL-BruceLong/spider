# -*- coding: utf-8 -*-
# @Time    : 2018-08-09 9:46
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_requests_正则—猫眼电影排行.py
# @Software: PyCharm
import json
import re
import time

import requests


def get_one_page(url):
    """获取第一页的内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    """正则筛选内容"""
    # 正则使用方法首在哪一个容器下面，其次就是找不同参数相同的值 用非贪婪的方法来找需要的数据
    # 此处用的格式:.*?相同的class或者id.*?>(.*?这里就是所需要的内容)以怎么结尾</i标签名>
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>',
        re.S
    )
    # 把产生的对象放到一个正则方法里findall（）方法是指匹配正则表达式的所有内容match()是用来手动写以字符串开始或结束
    # search()是指从开头扫描直到遇到第一个满足条件的就返回（不是全部哦）
    items = re.findall(pattern, html)
    # 把匹配的结果是一个列表，列表里是一个元组，把他再转换为一个字典存储起来
    for item in items:
        yield {
            "index": item[0],
            "image": item[1],
            "title": item[2].strip(),
            "actor": item[3].strip()[3:] if len(item[3]) > 3 else "",
            "time": item[4].strip()[5:] if len(item[4]) > 5 else "",
            "score": item[5].strip() + item[6].strip()

        }

        # print(iter())
    # print(items)


def write_to_file(content):
    """文件的存储"""
    with open("result.txt", "a", encoding="utf-8") as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + "\n")


def main(offset):
    """主程序"""
    # 给主页一个url
    url = "http://maoyan.com/board/4?offset=" + str(offset)

    # 获取第一页的内容
    html = get_one_page(url)
    # page = parse_one_page(html)
    # print(page)
    print(html)

    # 写入文件
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # 循环取出每一页的内容
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
