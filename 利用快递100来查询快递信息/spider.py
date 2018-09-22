# -*- coding: utf-8 -*-
# @Time    : 2018-08-26 9:16
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : spider.py
# @Software: PyCharm

import requests
import json

# 定义一个字典
KD_DICT = {1: 'shentong', 2: 'ems', 3: 'shunfeng', 4: 'yuantong', 5: 'zhongtong', 6: 'yunda', 7: 'tiantian',
           8: 'huitong', 9: 'quanfeng', 10: 'debang', 11: 'zhaijisong'}


def show_page():
    '''展示首页选择信息'''

    print('快递查询直通车：')
    print('-' * 20)
    print('1. 申通快递')
    print('2. EMS邮政快递')
    print('3. 顺丰递运')
    print('4. 圆通快递')
    print('5. 中通快递')
    print('6. 韵达快递')
    print('7. 天天快递')
    print('8. 汇通快递')
    print('9. 全峰快递')
    print('10. 德邦物流')
    print('11. 宅急送')
    print('0. 退出查询系统')
    print('-' * 20)


def execute_data_query(num):
    '''执行数据查询程序'''

    type = KD_DICT[num]
    postid = input('请输入您的快递单号：')
    # 通过构造一个真正的url地址
    url = 'http://www.kuaidi100.com/query?type=%s&postid=%s' % (type, postid)# 这里可以用元组这样保证的数据的安全性
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
        show_page()
        num = int(input('选择您的快递公司：'))
        while num not in range(12):
            num = int(input('选项有误，请重选：'))
        if num == 0:
            exit()
        else:
            execute_data_query(num)


if __name__ == '__main__':
    main()
