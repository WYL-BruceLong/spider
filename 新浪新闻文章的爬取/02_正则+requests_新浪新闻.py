# -*- coding: utf-8 -*-
# @Time    : 2018-08-12 20:46
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 02_正则+requests_新浪新闻.py
# @Software: PyCharm
import requests


def get_url_list(url):
    """
    根据url来获取子网页中的url列表
    :param url:
    :return:
    """
    # 报头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html_data = response.text.encode('gbk')
    print(html_data.decode('gbk'))


def main():
    """主程序"""
    # 初始化url
    url = 'https://www.sina.com.cn/'
    get_url_list(url)


if __name__ == '__main__':
    main()
