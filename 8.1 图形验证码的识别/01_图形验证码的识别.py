# -*- coding: utf-8 -*-
# @Time    : 2018-08-19 19:12
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_图形验证码的识别.py
# @Software: PyCharm
import pytesseract
from PIL import Image

# 打开文件这里只能是二进制形式
image = Image.open('code.jpg')
# 识别图片中的东西
result = pytesseract.image_to_string(image)
print(result)
