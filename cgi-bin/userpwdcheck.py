#!/usr/bin/python3
#encodin:utf-8
import sqlite3

userdata="userdata.sqlite"
def creat_data(database):
    with sqlite3.connect(database) as conn:
        cur=conn.cursor()
        cur.execute(u"drop table userdata")
        cur.execute(u"create table userdata(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id string,user_name string,pwd string)")
        cur.execute(u"insert into userdata(user_id,pwd,user_name) values(?,?,?)",["stevenfc@foxmail.com","qfc23834358","stevenfc"])
        cur.execute(u"insert into userdata(user_id,pwd,user_name) values(?,?,?)",["admin","23834358","管理员"])
        
def __init__():
    
    pass
    

def check(user_id="",pwd=""):
    with sqlite3.connect(userdata) as conn:
        cur=conn.cursor()
        cur.execute(u"select user_name,pwd from userdata where user_id=?",[user_id])
        res=cur.fetchone()
        if res:
            if pwd==res[1]:
                return True
            else:
                return False
        else:
            return False
