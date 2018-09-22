# -*- coding: utf-8 -*-
# @Time    : 2018-09-10 11:16
# @Author  : BruceLong
# @Email   : 18656170559@163.com
# @File    : demo.py
# @Software: PyCharm


import json

import requests

i = 1
while True:
    url = 'https://reader.browser.duokan.com/api/v2/chapter/content/4956/?chapterId={}&volumeId=0'.format(i)
    i += 1

    # 模拟浏览器来设置请求头
    headers = {
        'Host': 'reader.browser.duokan.com', 'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; Redmi S2 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.8.7',
        'Accept': '*/*', 'Referer': 'https', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': 'serviceToken=3SFRx9wbFrSQ6dFwDcQFr3vMK0rvvUqjVkTS8HEBgALb/hZ+chFGsh1RpwPiW1LVbQcBT8ORU1FjqxQwWsYts2kHtW2sJ96/sYMfT628rcqPEx1v+KNlT4Itkp7Eu6S95KuRBhilWQ3qYrlHF2m3XaXShl55xFYo/J3A5chwEiAwH0dDzlROnYzuqNPSGZbirjWs1gqiDmVfHmVY8srcCbU7F/nkGL56BocaOMYOHslYlehg/dAfviZ9nDxqDQSe; userId=77617265; browsernovel_slh=iv6ZZDHZyJqeTQZ9pxv+VbRj0ik=; browsernovel_ph=0HvNkZzFzH3MUB11xS4QxA=='

    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if data:

        title = data['data']['title']
        contentList = data['data']['contentList']
        print('标题：', title)
        print('文章正文：', contentList)
        print('')
    else:
        break
