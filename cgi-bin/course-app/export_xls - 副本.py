#!/usr/bin/python  
# -*- coding: <utf-8> -*- 
import xlwt
from mod.source import *
from xlrd import open_workbook
from xlutils.copy import copy
def generate_xls(path,head=[],table=[]):
    rb = open_workbook(path)
    #rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    sheet=ws
    """
    for c in range(17):
        sheet.col(c).width=256*20
    
    
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)  
    #sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)  ##第二参数用于确认同一个cell单元是否可以重设值。
    sheet = wbk.get_sheet('sheet 1')  ##第二参数用于确认同一个cell单元是否可以重设值。
    """
    style1 = xlwt.XFStyle()
    font = xlwt.Font()  
    font.name = '微软雅黑'  
    font.bold = True
    style1.font = font
    
    style2 = xlwt.XFStyle()
    font = xlwt.Font()  
    font.name = '微软雅黑'  
    font.bold = False
    x = 0
    for cell in head:
        sheet.write(0, x, cell,style1)
        x+=1
    y = 1
    for row in table:
        x = 0
        for cell in row:
            sheet.write(y, x, cell,style2)
            x+=1
        y += 1
      
    wb.save(path)
def get_data(self):
    table=[]
    for ei in self.filted_courses:
        table.append([ei.course_id,ei.course_name,ei.major,ei.course_type,ei.course_set,ei.course_tag,ei.level_range,ei.major_director,ei.head_instructor,ei.instructor_list,ei.state,ei.time_plan,ei.attendance_check,ei.homework,ei.examination,ei.file_path,ei.notes])
    return table    
head_lst=["课程编号","课程名称","专业","课程类型","系列",
          "系列标签","受训人","专业主管","课程负责人",
          "讲师","课程状态","时间计划","考勤","作业","考试","文件路径","备注"]
i=course_data()
i.course_set_code=i.major_code=i.level_selection="ALL"
i.get_results()
data=get_data(i)
path="./course_database.xls"
generate_xls(path,head_lst,data)
