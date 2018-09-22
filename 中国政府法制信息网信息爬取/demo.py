# -*- coding: utf-8 -*-
# @Time    : 2018-08-30 11:11
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : demo.py
# @Software: PyCharm
import re
import time

import requests

url_list = list()
def get_url_list(pageNum=4):
    global url_list
    url = 'http://www.chinalaw.gov.cn/col/col15/index.html?uid=1648&pageNum={}'.format(pageNum)
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        html = response.text
        one_pate_url_list = re.findall('<a target="_blank" href="(/art/.*?\.html)">', html)
        print(one_pate_url_list)
        print(len(one_pate_url_list))
        # if one_pate_url_list:
        #
        #     url_list.append(one_pate_url_list)
        #     print(url_list)
        #     pageNum += 3
        #     get_url_list(pageNum)
        # else:
        #     return url_list



        # if one_pate_url_list:
        #     yield one_pate_url_list
        #     pageNum += 3
        #     get_url_list(pageNum)
        # else:
        #     print('数据已经取完了')

    else:
        exit()


def main():
    '''主程序'''
    # while True:
    #
    #     for temp in get_url_list():
    #         print(temp)

    get_url_list()




if __name__ == '__main__':
    main()
