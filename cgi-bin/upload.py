#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests,os,sys,time

def main():
    try:
        with open("uploadpath.ini",'r+',encoding="gbk") as fr:
            dic = eval(fr.read())
            SerAddress,SaveDir=dic["SerAddress"],dic["SaveDir"]
            filepath=dic["filepath"].split(";")

        with open("upload.log","a+",encoding="gbk") as res:
            res.write("######\n")
            for file in filepath:
                c_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                with open(file,"rb") as f:
                    response = requests.post(SerAddress,data={'dirField':SaveDir,'fnField':os.path.basename(file)},files={'fileField':("tmp",f)})
                r_txt=response.text.strip()
                if r_txt=="Done":
                    res.write("##".join([c_time,file,"上传成功\n"]))
                else:
                    res.write("##".join([c_time,file,"上传失败："+r_txt+"\n"]))
    except FileNotFoundError:
        print("FileNotFoundError")

if __name__ == '__main__':
    main()
