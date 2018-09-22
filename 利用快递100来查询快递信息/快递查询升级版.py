# -*- coding: utf-8 -*-
# @Time    : 2018-08-26 9:16
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : spider.py
# @Software: PyCharm

import requests
import json


def get_express_type(postid):
    '''根据快递单号来智能判断快递类型'''
    url = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text=%s' % (postid,)  # 这里可以用元组这样保证的数据的安全性
    # 把构造后的url通过requests请求来得到相应的数据是一个json数据
    rs = requests.get(url)
    # 再用json库中的loads数据来进行分析得到一个可用字典的方式来访问
    kd_type_info = json.loads(rs.text)
    kd_type = kd_type_info['auto'][0]['comCode']
    return kd_type, postid


def execute_data_query(type, postid):
    '''执行数据查询程序'''

    # 通过构造一个真正的url地址
    url = 'http://www.kuaidi100.com/query?type=%s&postid=%s' % (type, postid)  # 这里可以用元组这样保证的数据的安全性
    # 把构造后的url通过requests请求来得到相应的数据是一个json数据
    rs = requests.get(url)
    # 再用json库中的loads数据来进行分析得到一个可用字典的方式来访问
    kd_info = json.loads(rs.text)
    msg = kd_info['message']
    # 判断是否成功获取到了json的数据，如果有数据则进行下一步的解析
    if msg == 'ok':
        print('您的快递%s物流信息如下：' % postid)
        data = kd_info['data']
        for data_dict in data:
            time = data_dict['time']
            context = data_dict['context']
            print('时间：%s %s' % (time, context))
    else:
        if msg == '参数错误':
            print('您输入信息有误，请重输：')
        else:
            print(msg)


def main():
    '''快递查询主程序'''
    while True:
        print('**欢迎您登录快递查询系统**')
        print('-' * 30)
        print('** 1. 请输入您的快递单号 **')
        print('** 0. 退出查询系统       **')
        print('-' * 30)
        order = input('查询请输入1退出请输入0：')
        if order == '1':
            # 进行快递查询操作
            postid = input('请输入您的快递单号：')
            type, postid = get_express_type(postid)
            execute_data_query(type, postid)
        elif order == '0':
            exit()
        else:
            print('!!!!!您的指令输入有误，请重新输入：<---------')


if __name__ == '__main__':
    main()
