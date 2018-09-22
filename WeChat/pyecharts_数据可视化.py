# -*- coding: utf-8 -*-
# @Time    : 2018-09-22 9:15
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : pyecharts_数据可视化.py
# @Software: PyCharm

# 导入Pie组件，用于生成饼图
import json

from pyecharts import Pie

# 获取所有性别
sex = []
with open('friends.json', mode='r') as  f:
    read_data = f.read()
    json_data = json.loads(read_data)
    for temp in json_data:
        str_sex = str(temp['Sex'])
        sex.append(str_sex)
# print(sex)
# 统计每个性别的数量
attr = ['帅哥', '美女', '未知']
value = [sex.count('1'), sex.count('2'), sex.count('0')]
pie = Pie('好友性别比例', '好友总人数：%d' % len(sex), title_pos='center')
pie.add('', attr, value, radius=[30, 75], rosetype='area', is_label_show=True,
        is_legend_show=True, legend_top='bottom')
# pie.show_config()
pie.render('好友性别比例.html')
