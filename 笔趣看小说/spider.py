# -*- coding: utf-8 -*-
# @Time    : 2018-08-27 22:29
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : spider.py
# @Software: PyCharm
# 第一步先获取第一章的文章的信息
# 第二步解析文章的内容
# 第三步下载数据
# 第四步把所有的章节都分析出来下载的链接
# 第五步循环下载
# 第六步开启多线程
# import gevent
# from gevent import monkey
# monkey.patch_all()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import threading

url = 'http://www.biqukan.com/1_1094/11303470.html'
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.get(url)


def get_one_page():
    '''
    获取第每一章的文章的信息
    :param url: 每一章的url
    :return: 返回一个html源码
    '''
    while True:

        # 判断是否有下一章这个按钮如果有就进行下一步操作
        if browser.find_element_by_css_selector('div.page_chapter > ul > li:nth-child(3) > a'):
            title = browser.find_element_by_tag_name('h1').text
            content = browser.find_element_by_id('content').text
            # print(title)

            print(title, '内容获取成功，开始下载')
            file_path = './一念永恒/' + title + '.txt'
            with open(file_path, 'w') as f:
                f.write(content)
            print(title, '文件下载成功')
            try:
                submit = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.page_chapter > ul > li:nth-child(3) > a'))
                )
                submit.click()
            except Exception as e:
                print('出错啦，原因是：', e)
        else:
            print('整个小说全部章节下载完成，请尽情享用吧@_@')
            browser.close()
            break


def main():
    '''一念永恒小说下载器'''

    # get_one_page()
    threading.Thread(target=get_one_page).start()


if __name__ == '__main__':
    main()
