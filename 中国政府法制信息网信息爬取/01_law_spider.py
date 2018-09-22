# -*- coding: utf-8 -*-
# @Time    : 2018-08-28 9:05
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_law_spider.py
# @Software: PyCharm

# 1.把正文解析并下载下来
# 2.数据分析保存到MongoDB中可以达到去重的目的
# 3.把每一个新闻的url地址爬取下来
# 4.把每一类的地址爬取下来

import pymongo
import requests
from pyquery import PyQuery as pq

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 保存到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'LawInformationDatabase'
MONGO_COLLECTION = 'DetailedInformation'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(result):
    '''
    保存到MongDB
    :param result:结果
    :return:
    '''
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception as e:
        print('存储到MongoDB失败，原因是：', e)


def get_one_page_text(url):
    '''
    根据url来获取一页的信息
    :param url: 文章的url
    :return: None
    '''
    response = requests.get(url, )
    response.encoding = 'utf-8'

    # 用pyquery来解析得到的网页信息源码
    doc = pq(response.text)

    # 标题
    title = doc('.art_tit').text().replace('\n', '')
    # 发布时间
    date = doc('span.sp_time > font:nth-child(1)').text().lstrip('日期：')
    # 信息来源
    source = doc('span.sp_time > font:nth-child(2)').text().lstrip('来源：')
    # 文章的正文内容
    content = doc('#zoom').text()
    # 把数据保存到MongoDB里面
    DetailedInformation = {
        'title': title,
        'date': date,
        'source': source,
        'content': content
    }
    print(DetailedInformation)
    save_to_mongo(DetailedInformation)


def get_each_page_url(index_url):
    '''
    获取每一页的url地址，因为这个列表的页面是经过js处理的不容易找到a标签的href属性
    所以用selenium，还有一个没有优化的是多任务和MongoDB的分类处理
    :param index_url: 首页的url地址
    :return: 返回每一页的url列表
    '''
    # 模拟浏览器来操作，如果在10秒内没有响应就结束
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    browser.get(index_url)

    while True:
        # 判断是否有下一页这个按钮如果有就进行下一步操作
        if browser.find_element_by_css_selector('.default_pgBtn.default_pgNext'):

            # 获取每个页面的a标签
            a = browser.find_elements_by_css_selector('.lmlb li a')

            # 得到每一个a标签解析得到href属性也就是需要的url地址
            for temp in a:
                url = temp.get_attribute('href')
                get_one_page_text(url)

            try:
                # 点击下一页
                submit = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.default_pgBtn.default_pgNext'))
                )
                submit.click()
            except Exception as e:
                print('出错啦，原因是：', e)
        else:
            print('整个法律下载完成，请尽情享用吧@_@')
            browser.close()
            break


def main():
    '''中国政府法制信息网信息爬取主程序'''
    # 首页的url
    index_url = 'http://www.chinalaw.gov.cn/col/col15/index.html?uid=1648&pageNum=1'
    get_each_page_url(index_url)
    # print(url)
    # print(len(url))
    # url = 'http://www.chinalaw.gov.cn/art/2018/8/27/art_15_209055.html'
    # get_one_page_text(url)


if __name__ == '__main__':
    main()
