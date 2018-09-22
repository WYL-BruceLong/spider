# -*- coding: utf-8 -*-
# @Time    : 2018-08-10 19:47
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_txt文本存储.py
# @Software: PyCharm
import requests
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
headers = {
    'user-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

# 为了让网页能模拟浏览器的操作来设置一个headers获取网页源码
html = requests.get(url, headers=headers).text

# 初始化，使用pyQuery来把html放到解析库里进行解析
doc = pq(html)
# 进行pyquery解析（里面放的是css选择器参数）对class里有两个参数来进行解析
items = doc('.explore-feed.feed-item').items()

# 循环遍历筛选后的数据
for item in items:
    # 提取里面的问题
    question = item.find('h2').text()
    # 提取里面的作者
    author = item.find('.author-link-line').text()
    # 提取里面的回复的内容，这里注意一下，在内容的上面有一个textarea被hidden了
    answer = pq(item.find('.content').html()).text()
# 方式一
    # 文件的存储以txt文本存储
    # file = open('explore.txt', 'a', encoding='utf-8')
    # # 文件的写入
    # file.write('\n'.join([question, author, answer]))
    # # 每一个内容用特殊符号隔开
    # file.write('\n' + '=' * 50 + '\n')
    # # 文件的关闭
    # file.close()

# 方式二
    # 简写的方法这样可以不用去关闭文件,系统已经封装好了关闭的方法
    with open('explore.txt', 'a', encoding='utf-8') as file:
        file.write('\n'.join([question, author, answer]))
        file.write('\n' + '=' * 50 + '\n')
