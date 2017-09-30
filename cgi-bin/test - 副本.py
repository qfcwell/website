#!/usr/bin/python
from cgi import FieldStorage
from os import environ
from cStringIO import StringIO
from urllib import quote, unquote
from string import capwords, strip, split, join
from time import ctime
 
class AdvCGI(object):
 
  header = 'Content-Type: text/html\n\n'  #定义头部
  url = 'upload.py'  #处理上传的文件名
 
  formhtml = '''<HTML><HEAD><TITLE>
    Advanced CGI Demo</TITLE></HEAD>
    <BODY><H2>Advanced CGI Demo Form</H2>
    <FORM METHOD=post ACTION="%s" ENCTYPE="multipart/form-data">
    <H3>Enter file to upload</H3>
    <INPUT TYPE=file NAME=upfile VALUE="%s" SIZE=45>
    <P><INPUT TYPE=submit>
    </FORM></BODY></HTML>'''  #表单基本html
 
  def showForm(self): # 显示上传表单
    print(AdvCGI.header + AdvCGI.formhtml % (AdvCGI.url,'NONE'))
 
  errhtml = '''<HTML><HEAD><TITLE>
      Advanced CGI Demo</TITLE></HEAD>
      <BODY><H3>ERROR</H3>
      <B>%s</B><P>
      <FORM><INPUT TYPE=button VALUE=Back
      ONCLICK="window.history.back()"></FORM>
      </BODY></HTML>'''
 
  def showError(self):  #显示错误提示
    print(AdvCGI.header + AdvCGI.errhtml % (self.error))
 
  reshtml = '''<HTML><HEAD><TITLE>
      Advanced CGI Demo</TITLE></HEAD>
      <BODY><H2>Your Uploaded Data</H2>
      <H3>Your uploaded file...<BR>
      Name: <I>%s</I><BR>
      Click <A HREF="%s"><B>here</B></A> to return to form.
      </BODY></HTML>'''
 
 
  def doResults(self):# 显示结果函数
    MAXBYTES = 1024000 #定义上传文件大小函数，单位为b
    filedata = ''  #初始化文件内容
    stop = ''  #初始化判断
    filename = self.fn  #获取文件名
    n = ctime()
    tmpname = '-'.join(n.split()[-1:]+n.split()[3].split(':'))+'.webtmp'  #设置需要保存文件名称，按日期保存
     
    while len(filedata) < MAXBYTES:# 读文件
      data = self.fp.readline()
      if data == '': break
      filedata += data
    else: # 如果超出文件大小
      error =  '... <B><I>(file truncated due to size)</I></B>' #提示
      self.showError() #显示错误信息
      stop = 'True' #停止
    self.fp.close() #关闭文件
    if filedata == '': #如果文件值为空
      filedata = \
       '<B><I>(file upload error or file not given)</I></B>'
      filename = self.fn
    if stop != 'True':  #这一步作判断，如果为真则保存文件，如果文件超出大小则不保存
      temp=open(tmpname,'w+')
      temp.write(filedata)
      temp.close()
      print(AdvCGI.header + AdvCGI.reshtml)
      (filename, AdvCGI.url)
 
  def go(self): # determine which page to return
    self.error = ''
    form = FieldStorage()
    if form.keys() == []:
      self.showForm()
      return
 
    if form.has_key('upfile'):
      upfile = form["upfile"]
      self.fn = upfile.filename or ''
      if upfile.file:
        self.fp = upfile.file
      else:
        self.fp = StringIO('(no data)')
    else:
      self.fp = StringIO('(no file)')
      self.fn = ''
 
    if not self.error:
      self.doResults()
    else:
      self.showError()
 
if __name__ == '__main__':
  page = AdvCGI()
  page.go()
