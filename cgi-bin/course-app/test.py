#!/usr/bin/python  
# -*- coding: <utf-8> -*-

database="cgi-bin/course_database.accdb"
import pyh,pypyodbc
import cgi,yate
from datetime import datetime
import content
try:
    post=cgi.FieldStorage()
    val = post["val"].value
except:
    val="ALL"
print(yate.start_response())
print(val)
