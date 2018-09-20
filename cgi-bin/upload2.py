#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests,os,sys,time

def main():
    try:
        with open("uploadpath.ini",'r+',encoding="gbk") as fr:
            dic = eval(fr.read())
            SerAddress,SaveDir="http://10.1.42.66/shenzhen/uploadservice2.py","样板图"
            #filepath=dic["filepath"].split(";")
            filepath=["D:\\桌面\\平台\\线上流程平台\\效果图确认单201801.xlsx"]

            with open("D:\\桌面\\平台\\线上流程平台\\效果图确认单201801.xlsx","rb") as f:
                #response = requests.post(url,data=f)
                response = requests.post(SerAddress,data=f)
                print(response.text)
            """
        with open("upload.log","a+",encoding="gbk") as res:
            res.write("######\n")
            for file in filepath:
                c_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                url="".join([SerAddress,"?","dirField=",SaveDir])
                with open(file,"rb") as f:
                    #response = requests.post(url,data=f)
                    response = requests.post(SerAddress,data={'file':("tmp",f)})
                    
                r_txt=response.text.strip()

                if r_txt=="Done":
                    res.write("##".join([c_time,file,"上传成功\n"]))
                else:
                    res.write("##".join([c_time,file,"上传失败："+r_txt+"\n"]))"""
    except FileNotFoundError:
        print("FileNotFoundError")

if __name__ == '__main__':
    main()
