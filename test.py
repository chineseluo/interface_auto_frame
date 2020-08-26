#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : interface_auto_frame
@Time    : 2020/8/26 14:23
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : test.py
@IDE     : PyCharm
------------------------------------
"""
import requests
import json

host = "http://httpbin.org/"
endpoint = "post"

url = ''.join([host, endpoint])
# 多文件上传
files = [
    ('file1', ('test.txt', open('D:\TestScriptDir\interface_auto_frame\Common\FileOption\comFileOption.py', 'rb'))),
    ('file2', ('test.png', open('D:\TestScriptDir\interface_auto_frame\Common\FileOption\yamlOption.py', 'rb')))
]

r = requests.post(url, files=files)
print(r.text)



