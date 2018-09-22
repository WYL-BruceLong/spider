# -*- coding: utf-8 -*-
# @Time    : 2018-08-31 9:08
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 02_law_spider(改良版).py
# @Software: PyCharm
import re


import requests
from multiprocessing import Pool
# post请求的参数
DATA = {
    'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '15', 'sourceContentType': '1',
    'unitid': '1648',
    'webname': '中国政府法制信息网', 'permissiontype': '0'
}

url_list = list()


def get_url_list(pageNum=1):
    global url_list

    # 请求的接口地址
    url = 'http://www.chinalaw.gov.cn/module/web/jpage/dataproxy.jsp?perpage=15&startrecord={}'.format(pageNum)

    # response = requests.post(url, data=data)
    response = requests.post(url, data=DATA)
    if response.status_code == 200:

        response.encoding = 'utf-8'
        html = response.text
        one_pate_url_list = re.findall('<a target="_blank" href="(/art/.*?\.html)">', html)
        print('从{}开始取出数据…………\n'.format(pageNum))
        print(one_pate_url_list)
        # 判断是否有数据有数据则保存下来
        if one_pate_url_list:
            # 把最后一个数据删除
            one_pate_url_list.pop()
            # 把本页的完整数据给保存到列表中
            url_list.append(one_pate_url_list)
            pageNum += 45
            get_url_list(pageNum)
        else:
            print('数据取完了')
            print(url_list)

    else:
        print('访问网站失败……')


def main():
    '''主程序'''
    get_url_list()


if __name__ == '__main__':
    main()
