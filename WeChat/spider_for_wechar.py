# -*- coding: utf-8 -*-
# @Time    : 2018-09-22 8:33
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : spider_for_wechar.py
# @Software: PyCharm

# 导入itchat模块，操作微信个人号的接口
import json

import itchat


# 获取数据
def get_data():
    # 扫描二维码登陆微信，实际上就是通过网页版微信登陆
    itchat.auto_login()
    # 获取所有好友信息
    friends = itchat.get_friends(update=True)  # 返回一个包含用户信息字典的列表
    return friends


# 处理数据
def parse_data(data):
    friends = []
    for item in data[1:]:  # 第一个元素是自己，排除掉
        friend = {
            'NickName': item['NickName'],  # 昵称
            'RemarkName': item['RemarkName'],  # 备注名
            'Sex': item['Sex'],  # 性别：1男，2女，0未设置
            'Province': item['Province'],  # 省份
            'City': item['City'],  # 城市
            'Signature': item['Signature'].replace('', ' ').replace(',', ' '),  # 个性签名（处理签名内容换行的情况）
            'StarFriend': item['StarFriend'],  # 星标好友：1是，0否
            'ContactFlag': item['ContactFlag']  # 好友类型及权限：1和3好友，259和33027不让他看我的朋友圈，65539不看他的朋友圈，65795两项设置全禁止
        }
        print(friend)
        friends.append(friend)
    return friends


# 存储数据，存储到文本文件
def save_to_txt():
    friends = parse_data(get_data())
    friends_json_data = json.dumps(friends)
    with open('friends.json', mode='a', encoding='utf-8') as f:
        f.write(friends_json_data)


if __name__ == '__main__':
    print(parse_data(get_data()))
    print(len(parse_data(get_data())))
    save_to_txt()
