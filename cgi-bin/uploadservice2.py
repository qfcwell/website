#!/usr/bin/python3
# -*- coding:utf-8 -*-
import cgi, os  
import cgitb; cgitb.enable()  

#try: # Windows needs stdio set for binary mode.  
import msvcrt  
import uuid  
msvcrt.setmode (0, os.O_BINARY) # stdin  = 0  
msvcrt.setmode (1, os.O_BINARY) # stdout = 1  
#except ImportError:  
#   pass  
  
form = cgi.FieldStorage()  
  
# Generator to buffer file chunks  
def fbuffer(f, chunk_size=10000):  
   while True:  
      chunk = f.read(chunk_size)  
      if not chunk: break  
      yield chunk  
  
# A nested FieldStorage instance holds the file  
fileitem = form['file']  
  
# Test if the file was uploaded  
if fileitem.filename:  
  
   # strip leading path from file name to avoid directory traversal attacks  
   fn = os.path.basename(fileitem.filename)  
    
   # Internet Explorer will attempt to provide full path for filename fix  
   fn = fn.split('\\')[-1]  
   
   # This path must be writable by the web server in order to upload the file.  
   path = 'C:/upload/'  
   filepath = path + fn  
  
   # Open the file for writing   
   f = open(filepath , 'wb', 10000)  
  
   # Read the file in chunks  
   for chunk in fbuffer(fileitem.file):  
      f.write(chunk)  
   f.close()  
  
  
   message = 'The file "' + fn + '" was uploaded successfully.'  
  
else:  
   message = 'No file was uploaded'  
  
print("""\nContent-Type: text/html\n 
<html><body> 
<p>%s</p> 
</body></html> 
""" % (message,))
