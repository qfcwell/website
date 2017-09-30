from datetime import datetime
import pypyodbc,pyh

def level_range_min(lst):
    i = 0
    if lst[i]:
        i=1
    else:
        while not lst[i]:
            i+=1
    return i
def level_range_max(lst):
    i = 0
    lst.reverse()
    while not lst[i]:
        i+=1
    return len(lst)-i

def res_convert(res):
    if isinstance(res,bool):
        if res:
            return "是"
        else:
            return "否"
    elif isinstance(res,datetime):
        res = res.strftime("%Y-%m-%d")
        return res
    elif isinstance(res,int):
        return str(res)
    elif res == None:
        return "-"
    else:
        return res
class codebox():
    def __init__(self):
        self.data=[]
        self.code_list=[]
        self.text_list=[]
        
    def feed(self,data):#传入(代号,中文)的列表
        self.data=data
        self.code_list=[]
        self.text_list=[]  
        for (code,text) in self.data:
            self.code_list.append(code)
            self.text_list.append(text)
        return self
    
    def get_text(self,in_code):#根据代号传出中文
        res=""
        if in_code in self.code_list:
            for (code,text) in self.data:
                if in_code==code:
                    res=text
        return res

    def get_code(self,in_text):#根据中文传出代号
        res=""
        if in_text in self.text_list:
            for (code,text) in self.data:
                if in_text==text:
                    res=code
        return res
    
database="C:/app_folder/website/course-app/cgi-bin/course_database.accdb"

class course():
    def __init__(self):
        self.database=database
        with pypyodbc.win_connect_mdb(self.database).cursor() as cur:           
            data1=cur.execute(u"SELECT major_code,major_name from major").fetchall()
            data2=cur.execute(u"SELECT set_id,set_name from course_set").fetchall()
            data3=cur.execute(u"SELECT type_id,type_text from course_type").fetchall()
            data4=cur.execute(u"SELECT state_id,state_type from state_type").fetchall()
        self.major_box=codebox().feed(data1)
        self.set_box=codebox().feed(data2)
        self.type_box=codebox().feed(data3)
        self.state_box=codebox().feed(data4)
        
    def get_data(self,course_id):
        self.course_id=course_id
        with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
            cur.execute(u"select course_id,course_name,major_code,type_code,course_set_code,course_tag,"
                    "level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,"
                    "major_director,head_instructor,instructor_list,course_state,state_code,"
                    "attendance_check,homework,examination,file_path,notes "
                    "from course where course_id=?",[self.course_id])
            self.data=cur.fetchone()
        if self.data:
            (course_id,self.course_name,self.major_code,self.type_code,self.course_set_code,self.course_tag,
             self.level_1,self.level_2,self.level_3,self.level_4,self.level_5,self.level_6,self.level_7,self.level_8,
             self.major_director,self.head_instructor,self.instructor_list,self.course_state,self.state_code,
             attendance_check,homework,examination,self.file_path,self.notes)=self.data
            level_list=[self.level_1,self.level_2,self.level_3,self.level_4,self.level_5,self.level_6,self.level_7,self.level_8]
            self.level_range="".join([str(level_range_min(level_list)),"~",str(level_range_max(level_list)),"级"])
            self.attendance_check=res_convert(attendance_check)
            self.homework=res_convert(homework)
            self.examination=res_convert(examination)
            self.major=self.major_box.get_text(self.major_code)
            self.course_type=self.type_box.get_text(self.type_code)
            self.course_set=self.set_box.get_text(self.course_set_code)
            self.state=self.state_box.get_text(self.state_code)
        else:
            self.course_name="未找到"
        return self
    
class course_data():
    def __init__(self):
        self.database=database
        self.course=course()
        self.courses=set()
        self.course_set_code="ALL"
        self.major_code="ALL"
        self.level_selection="ALL"
    def get_results(self):#生成过滤结果
        if self.database:
            with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
                cur.execute(u"select course_id,course_name,major_code,type_code,course_set_code from course")
                res=cur.fetchall()
                
                set1=set()
                set2=set()
                set3=set()
                
                set_box=self.course.set_box
                #major_box=codebox().feed(data2)
                for (course_id,course_name,major_code,course_type,course_set_code ) in res:
                    self.courses.add(course_id)
                    if self.course_set_code=="ALL" or self.course_set_code==course_set_code:    
                        set1.add(course_id)
                    if self.major_code=="ALL" or self.major_code==major_code:
                        set2.add(course_id)
                    if self.level_selection=="ALL":
                        set3.add(course_id)
                if self.level_selection != "ALL":
                    level=int(self.level_selection)
                    cur.execute(u"select course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8 from course")
                    res=cur.fetchall()
                    for (course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8) in res:
                        lst=[course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8]
                        if lst[level]:
                            set3.add(course_id)
                self.course_results=sorted(list(set1&set2&set3))
            return self.course_results
        else:
            return []   
    def get_results2(self):#生成过滤结果
        if self.database:
            with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
                cur.execute(u"select course_id,course_name,major_code,course_type,course_set_code from course")
                res=cur.fetchall()
                self.courses=set()
                self.courses_res=set()
                self.majors=set()
                self.course_types=set()
                self.course_sets=set()
                set1=set()
                set2=set()
                set3=set()
                data1=cur.execute(u"select set_id,set_name from course_set").fetchall()
                data2=cur.execute(u"select major_code,major_name from major").fetchall()
                set_box=codebox().feed(data1)
                major_box=codebox().feed(data2)
                for (course_id,course_name,major_code,course_type,course_set_code ) in res:
                    self.courses.add(course_id)
                    #self.majors.add(major)
                    self.course_types.add(course_type)
                    #self.course_sets.add(course_set)
                    if self.course_set_code=="ALL" or self.course_set_code==course_set_code:    
                        set1.add(course_id)
                    if self.major_code=="ALL" or major_box.get_text(self.major_code)==major:
                        set2.add(course_id)
                    if self.level_selection=="ALL":
                        set3.add(course_id)
                if self.level_selection != "ALL":
                    level=int(self.level_selection)
                    cur.execute(u"select course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8 from course")
                    res=cur.fetchall()
                    for (course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8) in res:
                        lst=[course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8]
                        if lst[level]:
                            set3.add(course_id)
                self.course_results=sorted(list(set1&set2&set3))
            return self.course_results
        else:
            return []
    def get_data3(self):#按结果过滤数据
        table=[]
        if self.database:
            i=course()
            for course_id in self.course_results:
                i.get_data(course_id)
                table.append([i.course_id,i.course_name,i.major,i.course_type,i.course_tag,i.level_range,i.major_director,i.head_instructor,i.instructor_list,i.course_state,i.attendance_check,i.homework,i.examination,i.file_path,i.notes])
        return table
    def get_data(self):#按结果过滤数据
        table=[]
        if self.database:
            i=course()
            with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
                 cur.execute(u"select course_id,course_name,major_code,type_code,course_set_code,course_tag,"
                    "level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,"
                    "major_director,head_instructor,instructor_list,state_code,"
                    "attendance_check,homework,examination,file_path,notes "
                    "from course order by course_id ASC")
                 res=cur.fetchall()
            for (course_id,course_name,major_code,type_code,course_set_code,course_tag,
                    level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,
                    major_director,head_instructor,instructor_list,state_code,
                    attendance_check,homework,examination,file_path,notes) in res:
                if course_id in self.course_results:
                    lst=[level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8]
                    level_range="".join([str(level_range_min(lst)),"~",str(level_range_max(lst)),"级"])
                    major=i.major_box.get_text(major_code)
                    course_type=i.type_box.get_text(type_code)
                    #course_set=i.set_box.get_text(course_set_code)
                    course_state=i.state_box.get_text(state_code)
                    table.append([course_id,course_name,major,course_type,course_tag,level_range,major_director,head_instructor,instructor_list,course_state,attendance_check,homework,examination,file_path,notes])
        return table

    def get_data2(self):#按结果过滤数据
        table=[]
        if self.database:
            with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
                 cur.execute(u"select course_id,course_name,major,course_type,course_tag,"
                    "level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,"
                    "major_director,head_instructor,instructor_list,course_state,"
                    "attendance_check,homework,examination,file_path,notes "
                    "from course "
                    "order by course_id ASC")
                 res=cur.fetchall()
            for (course_id,course_name,major,course_type,course_tag,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,major_director,head_instructor,instructor_list,course_state,attendance_check,homework,examination,file_path,notes) in res:
                if course_id in self.course_results:
                    lst=[level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8]
                    level_range="".join([str(level_range_min(lst)),"~",str(level_range_max(lst)),"级"])
                    table.append([course_id,course_name,major,course_type,course_tag,level_range,major_director,head_instructor,instructor_list,course_state,attendance_check,homework,examination,file_path,notes])
        return table

def generate_selection(set_selected="ALL",major_selected="ALL",level_selected="ALL"):
    with pypyodbc.win_connect_mdb(database).cursor() as cur:
        data1=cur.execute(u"select set_id,set_name from course_set").fetchall()
        data2=cur.execute(u"select major_code,major_name from major").fetchall()
    set_box=codebox().feed(data1)
    major_box=codebox().feed(data2)
    form=pyh.form(action="course_submit.py",method="POST")
    form<<"&nbsp;&nbsp;\n"
    
    form<<"<label>课程系列：</label>\n"
    selection=pyh.select(name="course_set_selection",style="min-width:10%")
    selection<<'<option value="ALL">全部</option>'
    for (set_id,set_name) in set_box.data:
        if set_id==set_selected:
            selection<<pyh.option(set_name,value=set_id,selected="T")
        else:
            selection<<pyh.option(set_name,value=set_id)
    form<<selection
    form<<"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    
    form<<"<label>专业：</label>"
    selection=pyh.select(name="major_selection",style="min-width:10%")
    
    selection<<'<option value="ALL">全部</option>'
    for (major_code,major_name) in major_box.data:
        if major_code==major_selected:
            selection<<pyh.option(major_name,value=major_code,selected="T")
        else:
            selection<<pyh.option(major_name,value=major_code)
    form<<selection
    form<<"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    
    form<<"<label>职级：</label>"
    selection=pyh.select(name="level_selection",style="min-width:10%")
    selection<<'<option value="ALL">全部</option>'
    for i in [1,2,3,4,5,6,7,8]:
        if str(i)==level_selected:
            selection<<pyh.option(str(i),value=str(i),selected="T")
        else:
            selection<<pyh.option(str(i),value=str(i))
    
    form<<selection
    form<<"&nbsp;&nbsp;&nbsp;&nbsp;"
    form<<'<input type="submit" value="查询">'
    return form

#i=course()
#i.get_data("PX0001")

#i=course_data()

#i.get_results()
#print(i.get_data())
