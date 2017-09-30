#!/usr/bin/python  
# -*- coding: <utf-8> -*-
from mod.source import *

import cgi,pypyodbc,pyh
from mod import yate,content
def thispage():
    print(yate.start_response())
    i=course()
    post=cgi.FieldStorage()
    i.course_id = post["course_id"].value
    old=course().get_data(i.course_id)
    try:
        i.course_name = post["course_name_input"].value
    except:
        i.course_name = old.course_name
    i.major_code = post["major_selection"].value
    i.type_code=post["type_selection"].value
    #i.course_set_code = post["set_selection"].value
    try:
        i.course_tag=post["course_tag_input"].value
    except:
        i.course_tag="-"
    res=post.getlist('level')
    i.level_1=i.level_2=i.level_3=i.level_4=i.level_5=i.level_6=i.level_7=i.level_8=False
    if res:
        if "1" in res:
            i.level_1=True
        if "2" in res:
            i.level_2=True
        if "3" in res:
            i.level_3=True
        if "4" in res:
            i.level_4=True
        if "5" in res:
            i.level_5=True
        if "6" in res:
            i.level_6=True
        if "7" in res:
            i.level_7=True
        if "8" in res:
            i.level_8=True
    try:
        i.major_director=post["major_director_input"].value
    except:
        i.major_director="-"
    try:
        i.head_instructor=post["head_instructor_input"].value
    except:
        i.head_instructor="-"
    try:
        i.instructor_list=post["instructors_input"].value
    except:
        i.instructor_list="-"
    try:
        i.time_plan=post["time_plan"].value
    except:
        i.time_plan="-"
    i.state_code=post["course_state_selection"].value
    
    res=post.getlist('assessment')
    i.attendance_check=i.homework=i.examination=False
    if res:
        if "attendance_check" in res:
            i.attendance_check=True
        if "homework" in res:
            i.homework=True
        if "examination" in res:
            i.examination=True
        
    try:
        i.file_path=post["file_path_input"].value
    except:
        i.file_path="-"   
    try:
        i.notes=post["notes_input"].value
    except:
        i.notes="-"   

    if i.submit_update():
        page=pyh.PyH('MINITECH STORM CLOUD')
        page.head += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
        page.head += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        page.head += '<meta http-equiv="refresh" content="0;url=course_info.py?course_id='+i.course_id+'"> '
        page.printOut()
    else:
        page=pyh.PyH('MINITECH STORM CLOUD')
        page.head += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
        page.head += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        page.head += '<meta http-equiv="refresh" content="0;url=course_list.py"> '
        page.printOut()

thispage()
