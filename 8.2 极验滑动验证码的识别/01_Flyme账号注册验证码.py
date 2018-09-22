# -*- coding: utf-8 -*-
# @Time    : 2018-08-20 8:27
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_Flyme账号注册验证码.py
# @Software: PyCharm
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

EMAIL = '17773456712'


# PASSWORD = '123456'


class CrackFlyme():
    def __init__(self):
        '''初始化'''
        self.url = 'https://i.flyme.cn/register'
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 10)
        self.email = EMAIL
        # self.password = PASSWORD

    def get_flyme_button(self):
        '''
        获取验证码按钮
        :return: 按钮对象
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_position(self):
        '''
        获取验证码位置
        :return: 验证码位置元组
        '''
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, button, left, right)

    def get_geetest_image(self, name='captcha.png'):
        '''
        获取验证码图片
        :param name:
        :return:  图片对象
        '''
        top, button, left, right = self.get_position()
        print('验证码位置：', top, button, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((top, button, left, right))
        return captcha

    def get_slider(self):
        '''
        获取滑块
        :return: 滑块对象
        '''
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def is_pixel_equal(self, image1, image2, x, y):
        '''
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        '''
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        '''
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 还缺口图片
        :return:
        '''
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        '''
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        '''
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初始速度为0
            v0 = v
            # 当前速度v = v0+at
            v = v0 + a * t
            # 移动距离x=v0t+1/2*a*t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        '''
        拖动滑块到缺口
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        '''
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()


flyme = CrackFlyme()
button = flyme.get_flyme_button()
button.click()
