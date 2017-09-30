#!/usr/bin/python3
#encodin:utf-8

import cgi,pyh
import userpwdcheck


print ("Content-type:text/html\r\n\r\n")

try:
    post=cgi.FieldStorage()
    username = post["username"].value
    pwd = post["password"].value
except:
    username=""
    pwd=""

if userpwdcheck.check(username,pwd):
    page=pyh.PyH('MINITECH STORM CLOUD')
    page.head += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
    page.head += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
    page.head += '<meta http-equiv="refresh" content="0;url=../hello.html"> '
    page.printOut()

else:
    page=pyh.PyH('MINITECH STORM CLOUD')
    page.head += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
    page.head += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
    page.head += '<meta http-equiv="refresh" content="0;url=../index.html"> '
    page.printOut()
    




