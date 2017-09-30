from datetime import datetime
import pypyodbc,pyh

css="../../css/style.course-app-red.css"
database="C:\\Users\\Administrator\\OneDrive\\website\\course_database.accdb"

def level_range_min(lst):
    i=0
    for ei in lst:
        i+=1
        if ei:
            return i
    return 0
def level_range_max(lst):
    lst.reverse()
    i=0
    for ei in lst:
        i+=1
        if ei:
            return len(lst)-i+1
    return 0

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

class course_box():
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

class course_set_box():
    def __init__(self):
        self.database=database
        self.dict={}
        with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
            cur.execute(u"select set_id,course_list from course_set")
            self.data=cur.fetchall()
            for (set_id,course_list) in self.data:
                self.dict[set_id]=course_list.split(",")
            
cb=course_box()
csb=course_set_box()
       
class course():
    def __init__(self):
        self.database=database
        self.major_box=cb.major_box
        self.set_box=cb.set_box
        self.type_box=cb.type_box
        self.state_box=cb.state_box
    
    def feed(self,tup):
        if tup:
            (self.course_id,self.course_name,self.major_code,self.type_code,self.course_tag,
             self.level_1,self.level_2,self.level_3,self.level_4,self.level_5,self.level_6,self.level_7,self.level_8,
             self.major_director,self.head_instructor,self.instructor_list,self.state_code,
             attendance_check,homework,examination,self.file_path,self.notes,self.time_plan)=tup
            level_list=[self.level_1,self.level_2,self.level_3,self.level_4,self.level_5,self.level_6,self.level_7,self.level_8]
            self.level_range="".join([str(level_range_min(level_list)),"~",str(level_range_max(level_list)),"级"])
            self.attendance_check=res_convert(attendance_check)
            self.homework=res_convert(homework)
            self.examination=res_convert(examination)
            self.major=self.major_box.get_text(self.major_code)
            self.course_type=self.type_box.get_text(self.type_code)
            #self.course_set=self.set_box.get_text(self.course_set_code)
            self.state=self.state_box.get_text(self.state_code)
            course_set=[]
            for ei in csb.dict:
                if self.course_id in csb.dict[ei]:
                    course_set.append(self.set_box.get_text(ei))
            self.course_set=",".join(course_set)
	
        return self
    def get_data(self,course_id):
        self.course_id=course_id
        with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
            cur.execute(u"select course_id,course_name,major_code,type_code,course_tag,"
                            "level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,"
                            "major_director,head_instructor,instructor_list,state_code,"
                            "attendance_check,homework,examination,file_path,notes,time_plan "
                            "from course where course_id=?",[course_id])
            self.data=cur.fetchone()
            self.feed(self.data)
        return self
    
    def submit_update(self):
        try:
            with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
                cur.execute(u"update course set course_name=?,major_code=?,type_code=?,course_tag=?,"
                            "level_1=?,level_2=?,level_3=?,level_4=?,level_5=?,level_6=?,level_7=?,level_8=?,"
                            "major_director=?,head_instructor=?,instructor_list=?,state_code=?,time_plan=?,"
                            "attendance_check=?,homework=?,examination=?,file_path=?,notes=? "
                            "where course_id=?",[self.course_name,self.major_code,self.type_code,self.course_tag,
                            self.level_1,self.level_2,self.level_3,self.level_4,self.level_5,self.level_6,self.level_7,self.level_8,
                            self.major_director,self.head_instructor,self.instructor_list,self.state_code,self.time_plan,
                            self.attendance_check,self.homework,self.examination,self.file_path,self.notes,self.course_id])
            return True
        except:
            return False
    
class course_data():
    def __init__(self):
        self.database=database
        self.course=course()
        self.courses=[]
        self.course_set_selection="ALL"
        self.major_code="ALL"
        self.level_selection="ALL"
        if self.database:
            with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
                cur.execute(u"select course_id,course_name,major_code,type_code,course_tag,"
                            "level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8,"
                            "major_director,head_instructor,instructor_list,state_code,"
                            "attendance_check,homework,examination,file_path,notes,time_plan "
                            "from course order by course_id ASC")
                self.all_data=cur.fetchall()
            for row in self.all_data:
                self.courses.append(course().feed(row))

        
    def get_results(self):#生成过滤结果
        if self.database:
            with pypyodbc.win_connect_mdb(self.database).cursor() as cur:
                cur.execute(u"select course_id,course_name,major_code,type_code from course")
                res=cur.fetchall()
                
                set1=set()
                set2=set()
                set3=set()
                
                set_box=self.course.set_box
                #major_box=codebox().feed(data2)
                
                for (course_id,course_name,major_code,course_type) in res:
                    #self.courses.add(course_id)
                    set1.add(course_id)
                    if self.major_code=="ALL" or self.major_code==major_code:
                        set2.add(course_id)
                    if self.level_selection=="ALL":
                        set3.add(course_id)
                if self.course_set_selection !="ALL":
                    cur.execute(u"select set_id,course_list from course_set where set_id=?",[self.course_set_selection])
                    set_id,course_list = cur.fetchone()
                    set1=set(course_list.split(","))
                if self.level_selection != "ALL":
                    level=int(self.level_selection)
                    cur.execute(u"select course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8 from course")
                    res=cur.fetchall()
                    for (course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8) in res:
                        lst=[course_id,level_1,level_2,level_3,level_4,level_5,level_6,level_7,level_8]
                        if lst[level]:
                            set3.add(course_id)
                self.course_results=sorted(list(set1&set2&set3))
            self.filted_courses=[]
            for course in self.courses:
                if course.course_id in self.course_results:
                    self.filted_courses.append(course)
            return self.filted_courses
        else:
            return []
      
    


def generate_selection(set_selected="ALL",major_selected="ALL",level_selected="ALL"):
    set_box=cb.set_box
    major_box=cb.major_box
    
    form=pyh.form(action="course_list.py",method="POST")
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


