#!/usr/bin/python  
# -*- coding: <utf-8> -*-
import pypyodbc,pyh
from mod import yate,content
from mod.source import *

#with pypyodbc.win_connect_mdb(database).cursor() as cur:
    cur.execute(u"select course_type from course")
    res=cur.fetchall()
    for (course_type,)in res:
        cur.execute(u"select type_id from course_type where type_text=?",[course_type])
        res2=cur.fetchone()
        if res2:
            (resss)=res
            cur.execute("update course set type_code=? where course_type=?",[resss,course_type])


        
        
