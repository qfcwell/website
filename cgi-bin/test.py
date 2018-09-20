#!/usr/bin/python3

print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Hello Word - First CGI Program</title>')
print("""<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
""")
print ('</head>')
print ('<body>')
print ('<h2>Hello Word! This is my first CGI program</h2>')


print("""<form method="post">
        <input type="text" name="path">
        <input type="file" name="myfile"><br>
        <input type="submit" value="上传">
    </form> """)
try:
    post=cgi.FieldStorage()
    result = post["fileField"].value
    
    #i.level_selection="ALL"
except:
    result="1111"
print(result)
print ('</body>')
print ('</html>')
