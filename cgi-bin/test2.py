#!/usr/bin/python3
import cgi,pypyodbc,os
print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Hello Word - First CGI Program</title>')
print("""<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />""")
print ('</head>')
print ('<body>')
print ('<h2>Hello Word! This is my first CGI program</h2>')


print("""<div class="file-box"> 
<form action="test2.py" method="post" enctype="multipart/form-data"> 
<input type='text' name='textfield' id='textfield' class='txt' /> 
<input type='button' class='btn' value='浏览...' /> 
<input type="file" name="fileField" class="file" id="fileField" size="28" onchange="document.getElementById('textfield').value=this.value" /> 
<input type="submit" name="submit" class="btn" value="上传" /> 
</form> 
</div> """)
post=cgi.FieldStorage()
result = post["fileField"]
fn = os.path.basename(result.filename)
with open("C:/"+fn,"wb") as file:
  file.write(result.file.read())
#print(result.readline())
print ('</body>')
print ('</html>')
