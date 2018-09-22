# -*- coding: utf-8 -*-
# @Time    : 2018-08-19 19:12
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : 01_图形验证码的识别.py
# @Software: PyCharm
import pytesseract
from PIL import Image

# 打开图片以二进制形式
image = Image.open('CheckCode.jpg')
# 把原图片转化为灰度图像，image.convert()方法参数传入L
image = image.convert('L')
# 图像的二值化，就是将图像上的像素点的灰度值设置为0或255，也就是将整个图像呈现出明显的只有黑和白的视觉效果。
# 这里是指定二值化的阈值为127
threshold = 127
# 用来存储数据
table = []
# 与阈值对比
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
image.show()


result = pytesseract.image_to_osd(image)
print(result)
