#!/usr/bin/python3
# -*- coding:utf-8 -*-
import cgi,os
print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Hello Word - First CGI Program</title>')
print("""<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
""")
print ('</head>')
print ('<body>')

print("""<div class="file-box"> 
<form action="test2.py" method="post"> 
<input type='text' name='dirField' /> 
<input type="file" name="fileField" onchange="document.getElementById('textfield').value=this.value" /> 
<input type="submit" name="submit" class="btn" value="上传" /> 
</form> 
</div> """)
post=cgi.FieldStorage()
file_dir = post["dirField"].value
result = post["fileField"]
file_name = os.path.basename(result.filename)
file = result.file.read()
print(file_dir)

if not os.path.isdir(file_dir):
    try:
        os.makedirs(file_dir)
    except:
        print("文件路径错误") 

path=os.path.join(file_dir,file_name)

if os.path.exists(path):#覆盖文件
    try:
        os.remove(path)
        #file.save(path)
        with open(path,"wb") as target:
            target.write(file)
    except:
        print("目标为文件夹")
else:
    with open(path,"wb") as target:
        target.write(file)
    #file.save(path)


print ('</body>')
print ('</html>')
