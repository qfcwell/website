#!/usr/bin/python  
# -*- coding: <utf-8> -*-
from mod.source import *

import cgi,pypyodbc,pyh
from mod import yate,content
def thispage():
    print(yate.start_response())
    def get_post():
        try:
            post=cgi.FieldStorage()
            course_id = post["course_id"].value
            #i.major_code = post["major"].value
            #i.level_selection = post['level_selection'].value
            #i.level_selection="ALL"
            #i=course()
            i=course().get_data(course_id)
            return i
        except:
            i=course().get_data("PX0001")
            return i


    i=get_post()

    js=["js/plugins/jquery-1.7.min.js","js/plugins/jquery-ui-1.8.16.custom.min.js","js/plugins/jquery.cookie.js",
        "js/plugins/jquery.uniform.min.js","js/plugins/jquery.flot.min.js","js/plugins/jquery.flot.resize.min.js",
        "js/plugins/jquery.slimscroll.js","js/custom/general.js","js/custom/dashboard.js"]

    page=pyh.PyH(i.course_id+i.course_name)
    page.head += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
    page.head += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
    page.addCSS(css)
    for js in js:
        page.addJS("../../"+js)
    page.head+=content.if_ie987
    #page.head += '<style type="text/css">form input[type=text] { border: 1px solid #ddd; padding: 7px 5px 8px 5px; width: 200px; background: #fff; }form select{min-width:5%;}</style>'

    bodywrapper=pyh.div(cl="bodywrapper")

    topheader=pyh.div(cl="topheader")
    topheader << content.head_left
    topheader << content.head_right
    bodywrapper<<topheader
    breadcrumbs=pyh.ul(cl="breadcrumbs")
    breadcrumbs<<'<li><a href="../../app.html">工作空间</a></li><li> <a href="course_list.py">培训课程</a></li>'
    breadcrumbs<<pyh.li()<<pyh.a(i.course_id+" "+i.course_name,href="#")
    bodywrapper<<breadcrumbs

    bodywrapper<<pyh.div('<ul class="hornav" style="margin-top:0px; padding:10px 10px 0px 10px">'
                         '<li class="current"><a href="#course_info">课程信息</a></li>'
                         '<li> <a href="#course_record">课程记录</a></li></ul>',style="background:#fcfcfc")

    contentwrapper=pyh.div(cl="contentwrapper",id="contentwrapper")
    course_info=pyh.div(id="course_info",cl="subcontent")
    two_third=pyh.div(cl="two_third dashboard_left")
    two_third<<pyh.div("<h3>"+i.course_id+" "+i.course_name+"</h3>",cl="contenttitle2 nomargintop")

    form=pyh.form(cl="stdform stdform2",method="post",action="course_update.py")
    form<<pyh.p("<label>课程编号<small>COURSE ID</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="course_id_input",id="course_id_input",cl="smallinput",value=i.course_id,disabled="disabled")
    form<<pyh.input(type="hidden",name="course_id",id="course_id",value=i.course_id)
    form<<pyh.p("<label>课程名称<small>COURSE NAME</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="course_name_input",id="course_name_input",cl="mediuminput",value=i.course_name)
    major_selection=pyh.select(type="text",name="major_selection",id="major_selection")
    for (code,text) in cb.major_box.data:
        if code==i.major_code:
            major_selection<<pyh.option(text,value=code,selected="T")
        else:
            major_selection<<pyh.option(text,value=code)   
    form<<pyh.p("<label>专业<small>MAJOR</small></label>")<<pyh.span(cl="field")<<major_selection
    type_selection=pyh.select(type="text",name="type_selection",id="type_selection")
    for (code,text) in cb.type_box.data:
        if code==i.type_code:
            type_selection<<pyh.option(text,value=code,selected="T")
        else:
            type_selection<<pyh.option(text,value=code)   
    form<<pyh.p("<label>课程类型<small>COURSE TYPE</small></label>")<<pyh.span(cl="field")<<type_selection
    """
    set_selection=pyh.select(type="text",name="set_selection",id="set_selection")
    for (code,text) in cb.set_box.data:
        if code==i.course_set_code:
            set_selection<<pyh.option(text,value=code,selected="T")
        else:
            set_selection<<pyh.option(text,value=code)
    form<<pyh.p("<label>所属系列<small>COURSE SET</small></label>")<<pyh.span(cl="field")<<set_selection
    """

    form<<pyh.p("<label>标签<small>TAG</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="course_tag_input",id="course_tag_input",cl="mediuminput",value=i.course_tag)

    trainees=pyh.span(cl="field")
    """
    if i.level_1:
        trainees<<pyh.input(type="checkbox",name="level_1",checked="checked")
    else:
        trainees<<pyh.input(type="checkbox",name="level_1")
    trainees<<"1级 &nbsp;"
    """
    k=0
    for ei in [i.level_1,i.level_2,i.level_3,i.level_4,i.level_5,i.level_6,i.level_7,i.level_8]:
        k+=1
        if ei:
            trainees<<pyh.input(type="checkbox",name="level",value=k,checked="checked")
        else:
            trainees<<pyh.input(type="checkbox",name="level",value=k)
        trainees<<pyh.span(str(k)+"级",style="vertical-align:middle;margin-right:10px")

    form<<pyh.p("<label>受训人<small>TRAINEES</small></label>")<<trainees
    form<<pyh.p("<label>专业主管<small>DIRECTOR</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="major_director_input",id="major_director_input",cl="smallinput",value=i.major_director)
    form<<pyh.p("<label>课程负责人<small>HEAD INSTRUCTOR</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="head_instructor_input",id="head_instructor_input",cl="smallinput",value=i.head_instructor)
    form<<pyh.p("<label>讲师<small>INSTRUCTORS</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="instructors_input",id="instructors_input",cl="longinput",value=i.instructor_list)
    course_state=pyh.select(type="text",name="course_state_selection",id="course_state_selection")
    for (code,text) in cb.state_box.data:
        if code==i.state_code:
            course_state<<pyh.option(text,value=code,selected="T")
        else:
            course_state<<pyh.option(text,value=code)   
    form<<pyh.p("<label>课程状态<small>COURSE STATE</small></label>")<<pyh.span(cl="field")<<course_state
    form<<pyh.p("<label>课件时间计划<small>TIME PLAN</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="time_plan",id="itime_plan",cl="longinput",value=i.time_plan)
    assess=pyh.span(cl="field")
    if i.attendance_check=="是":
        assess<<pyh.input(type="checkbox",name="assessment",value="attendance_check",checked="checked")
    else:
        assess<<pyh.input(type="checkbox",name="assessment",value="attendance_check")
    assess<<"考勤 &nbsp;"
    if i.homework=="是":
        assess<<pyh.input(type="checkbox",name="assessment",value="homework",checked="checked")
    else:
        assess<<pyh.input(type="checkbox",name="assessment",value="homework")
    assess<<"作业 &nbsp;"
    if i.examination=="是":
        assess<<pyh.input(type="checkbox",name="assessment",value="examination",checked="checked")
    else:
        assess<<pyh.input(type="checkbox",name="assessment",value="examinationk")
    assess<<"考试 &nbsp;"
    form<<pyh.p("<label>考核方式<small>ASSESSMENT</small></label>")<<assess
    form<<pyh.p("<label>文件路径<small>FILE PATH</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="file_path_input",id="file_path_input",cl="longinput",value=i.file_path)
    form<<pyh.p("<label>备注<small>NOTES</small></label>")<<pyh.span(cl="field")<<pyh.input(type="text",name="notes_input",id="notes_input",cl="longinput",value=i.notes)
    form<<'<p class="stdformbutton" ><input type="submit"  value="提交">&nbsp;&nbsp;&nbsp;&nbsp;<a href="course_info.py?course_id='+i.course_id+'">取消</a></p>'
    two_third<<form
    course_info<<two_third
    one_third=pyh.div(cl="one_third last dashboard_right")
    one_third<<'<div class="contenttitle2 nomargintop" style="display: none;"> <h3>培训记录</h3> </div><!--contenttitle-->'
    course_info<<one_third
    course_record=pyh.div(id="course_record",cl="subcontent",style="display: none;")
    contentwrapper<<course_info
    contentwrapper<<course_record
    bodywrapper<<contentwrapper 
    page<<bodywrapper
    page.printOut()
thispage()
