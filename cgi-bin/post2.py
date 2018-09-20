#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests,os,sys,time
from uploadpath import *

with open("uploadpath.py","a",encoding="utf-8") as res:
    for file in filepath:
        c_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        with open(file,"rb") as f:
            response = requests.post(SerAddress,data={'dirField':SaveDir,'fnField':os.path.basename(file)},files={'fileField':("tmp",f)})
        r_txt=response.text.strip()
        if r_txt=="Done":
            res.write("##".join(["\n#",c_time,file,"上传成功"]))
        else:
            res.write("##".join(["\n#",c_time,file,"上传失败："+r_txt]))
