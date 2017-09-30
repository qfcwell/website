#!/usr/bin/python  
# -*- coding: <utf-8> -*-
from mod.source import *

import cgi,pypyodbc,pyh
from mod import yate,content

with pypyodbc.win_connect_mdb(database).cursor() as cur:
    cur.execute(u"select set_id,set_name from course_set")
    res=cur.fetchall()
    
    for (set_id,set_name) in res:
        lst=[]
        cur.execute(u"select course_id,course_set_code from course where course_set_code=?",[set_id])
        for (course_id,course_set_code) in cur.fetchall():
            lst.append(course_id)
        cur.execute(u"update course_set set course_list=? where set_id=?",[",".join(lst),set_id])
   
