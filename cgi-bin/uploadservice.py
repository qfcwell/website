#!/usr/bin/python3
# -*- coding:utf-8 -*-

import cgi,os,sys

def read_and_write_file(post,path):
    result = post["fileField"]
    file = result.file.read()
    with open(path,"wb") as target:
        target.write(file)
        print("Done")

print("\n")
post=cgi.FieldStorage()
file_dir = post["dirField"].value
file_dir=os.path.join(sys.path[0],file_dir)
file_name = post["fnField"].value
path=os.path.join(file_dir,file_name)

if not os.path.isdir(file_dir):
    try:
        os.makedirs(file_dir)
    except:
        print("目标文件路径有问题") 

if os.path.exists(path):#覆盖文件
    try:
        os.remove(path)
        read_and_write_file(post,path)
    except:
        print("目标与文件夹同名？")
else:
    read_and_write_file(post,path)


