#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests

from uploadpath import *

postData = {
    'dirField':'C:\\Work\\11',
}
files={'fileField':("images.zip", open(r"D:\2016工时.xlsx", "rb"))}


response = requests.post('http://10.1.42.66/test2/cgi-bin/test2.py',data=postData,files=files)
print(response.text)