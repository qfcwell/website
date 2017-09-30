#!/usr/bin/python  
# -*- coding: <utf-8> -*-
from mod.source import *

import cgi,pypyodbc,pyh
from mod import yate,content

#database="C:/app_folder/website/course-app/cgi-bin/course_database.accdb"

def colgroup(lst,start=0):
    s=sum(lst)
    if s != 100:
        res=[]
        for ei in lst:
            res.append(ei*100/s)
        lst=res
    myclg=pyh.colgroup()
    for ei in lst:
        myclg << pyh.col(cl="con"+str(start),style="width: "+str(ei)+"%")
    return myclg



def theadfoot(lst,start=0):
    mythead=pyh.thead()
    mytfoot=pyh.tfoot()
    mytr=pyh.tr()
    for ei in lst:
        mytr << pyh.th(res_convert(ei),cl="head"+str(start))
    mythead<<mytr
    mytfoot<<mytr
    return [mythead,mytfoot]

def table_data(data):
    
    tbody=pyh.tbody()
    for row in data:
        tr = pyh.tr(cl="gradeA")
        i=1
        for ei in row:
            if i==2:
                a=pyh.a(res_convert(ei),href="courses/"+row[0]+".py")
                tr<<pyh.td(a)
            elif i in [5,9,10,14,15]:
                tr<<pyh.td(res_convert(ei))
            else:
                tr<<pyh.td(res_convert(ei),style="text-align:center;")
            i+=1
   
        tbody<<tr
        
    return tbody


print(yate.start_response())


clg_lst=[4,22,5,4,7,4,4,5,10,8,3,3,3,12,6]
head_lst=["课程编号","课程名称","专业","课程类型",
          "系列标签","受训人","专业主管","课程负责人",
          "讲师","课程状态","考勤","作业","考试","文件路径","备注"]
def data():
    i=course_data()
    try:
        post=cgi.FieldStorage()
        i.course_set_code = post["course_set_selection"].value
        i.major_code = post["major_selection"].value
        i.level_selection = post['level_selection'].value
        #i.level_selection="ALL"
    except:
        i.course_set_code=i.major_code=i.level_selection="ALL"
    i.get_results()
    return i

i=data()
data=i.get_data()


page=pyh.PyH('study center')
page.head += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
page.head += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
page.addCSS('../css/style.default-red.css')
for js in content.js:
    page.addJS(js)
page.head+=content.if_ie987
page.head += '<style type="text/css">form input[type=text] { border: 1px solid #ddd; padding: 7px 5px 8px 5px; width: 200px; background: #fff; }form select{min-width:5%;}</style>'

bodywrapper=pyh.div(cl="bodywrapper")

topheader=pyh.div(cl="topheader")
topheader << content.head_left
topheader << content.head_right
bodywrapper<<topheader
bodywrapper<<pyh.ul(cl="breadcrumbs")<<'<li><a href="#">工作空间</a></li><li> <a href="#">培训课程</a></li>'
bodywrapper<<pyh.div('<ul class="hornav" style="margin-top:0px; padding:10px 10px 0px 10px">'
                     '<li class="current"><a href="work.html">培训课程</a></li>'
                     '<li> <a href="manage.html">培训记录</a></li></ul>',style="background:#fcfcfc")
contentwrapper=pyh.div(cl="contentwrapper",id="contentwrapper")
div=pyh.div(cl="dataTables_length",style="padding:5px")
div<<generate_selection(i.course_set_code,i.major_code,i.level_selection)
contentwrapper<<div
mytable=pyh.table(cellpadding="0",cellspacing="0",border="0",cl="stdtable",id="dyntable")
myclg=colgroup(clg_lst,start=0)
head,foot = theadfoot(head_lst)

tbody=table_data(data)#table

mytable<<myclg
mytable<<head
mytable<<foot
mytable<<tbody

form=pyh.form()
form<<mytable
contentwrapper << form

bodywrapper<<contentwrapper 
page<<bodywrapper
output=page.output()

page.printOut()
      
#print(i.course_set_code)
