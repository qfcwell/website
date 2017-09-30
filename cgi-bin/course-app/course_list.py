#!/usr/bin/python  
# -*- coding: <utf-8> -*-
from mod.source import *

import cgi,pypyodbc,pyh
from mod import yate,content


print(yate.start_response())

def thispage():
    clg_lst=[8,26,5,5,5,5,6,12,10,10,8]
    head_lst=["课程编号","课程名称","专业","课程类型",
              "受训人","专业主管","课程负责人",
              "讲师","课程状态","课件时间计划","备注"]
    def data():
        i=course_data()
        try:
            post=cgi.FieldStorage()
            i.course_set_selection = post["course_set_selection"].value
            i.major_code = post["major_selection"].value
            i.level_selection = post['level_selection'].value
            #i.level_selection="ALL"
        except:
            i.course_set_selection=i.major_code=i.level_selection="ALL"
        i.get_results()
        return i

    def table_data(self):
        tbody=pyh.tbody()
        for ei in self.filted_courses:
            tr = pyh.tr(cl="gradeA")
            tr<< pyh.td(ei.course_id,style="text-align:center;")
            tr<< pyh.td()<<pyh.a(ei.course_name,href="course_info.py?course_id="+ei.course_id)
            tr<< pyh.td(ei.major,style="text-align:center;")
            tr<< pyh.td(ei.course_type,style="text-align:center;")
            tr<< pyh.td(ei.level_range,style="text-align:center;")
            tr<< pyh.td(ei.major_director,style="text-align:center;")
            tr<< pyh.td(ei.head_instructor,style="text-align:center;")
            tr<< pyh.td(ei.instructor_list)
            tr<< pyh.td(ei.state)
            tr<< pyh.td(ei.time_plan)
            tr<< pyh.td(ei.notes)
            tbody<<tr       
        return tbody

    i=data()
    #data=get_data(i)


    page=pyh.PyH('study center')
    page.head += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
    page.head += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
    page.addCSS(css)
    js=['../../js/plugins/jquery-1.7.min.js',
        '../../js/plugins/jquery-ui-1.8.16.custom.min.js',
        '../../js/plugins/jquery.cookie.js',
        '../../js/plugins/jquery.dataTables.min.js',
        '../../js/plugins/jquery.uniform.min.js',
        '../../js/custom/general.js',
        "../../js/custom/tables.js"]
    for ei in js:
        page.addJS(ei)
    page.head+=content.if_ie987

    bodywrapper=pyh.div(cl="bodywrapper")

    topheader=pyh.div(cl="topheader")
    topheader << content.head_left
    topheader << content.head_right
    bodywrapper<<topheader
    breadcrumbs=pyh.ul(cl="breadcrumbs")
    breadcrumbs<<'<li><a href="../../app.html">工作空间</a></li><li> <a href="course_list.py">培训课程</a></li>'
    bodywrapper<<breadcrumbs
    bodywrapper<<pyh.div('<ul class="hornav" style="margin-top:0px; padding:10px 10px 0px 10px">'
                         '<li class="current"><a href="#course_list">培训课程</a></li>'
                         '<li> <a href="#records">培训记录</a></li></ul>',style="background:#fcfcfc")
    contentwrapper=pyh.div(cl="contentwrapper",id="contentwrapper")
    course_list=pyh.div(cl="subcontent",id="course_list")
    div=pyh.div(cl="dataTables_length",style="padding:5px")
    div<<generate_selection(i.course_set_selection,i.major_code,i.level_selection)
    course_list<<div
    mytable=pyh.table(cellpadding="0",cellspacing="0",border="0",cl="stdtable",id="dyntable3")
    myclg=colgroup(clg_lst,start=0)
    head,foot = theadfoot(head_lst)
    tbody=table_data(i)#table
    mytable<<myclg
    mytable<<head
    mytable<<foot
    mytable<<tbody
    course_list << mytable
    record=pyh.div(cl="subcontent",id="records",style="display:none;")
    #div=pyh.div(cl="dataTables_length",style="padding:5px")
    #div<<generate_selection(i.course_set_code,i.major_code,i.level_selection)
    #record<< div
    clg_lst=[6,6,6,28,6,6,8,14,10,10]
    head_lst=["记录编号","培训时间","课程编号","课程名称","专业","课程类型",
              "课程负责人","讲师","参训人名单","备注"]
    mytable=pyh.table(cellpadding="0",cellspacing="0",border="0",cl="stdtable",id="dyntable2")
    myclg=colgroup(clg_lst,start=0)
    head,foot = theadfoot(head_lst)
    data=[("-","-","-","-","-","-","-","-","-","-")]

    #tbody=table_data(i)#table
    mytable<<myclg
    mytable<<head
    mytable<<foot
    #mytable<<tbody
    record << mytable
    contentwrapper << course_list
    contentwrapper << record
    bodywrapper<<contentwrapper 
    page<<bodywrapper
    page.printOut()
    
thispage()
