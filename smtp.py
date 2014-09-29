#!/usr/bin/python
#-*- coding:utf-8 -*-
from email.mime.text import MIMEText
msg=MIMEText('hello,send by python..','plain','utf-8')
from_addr=raw_input('from:')
password =raw_input('password:')
smtp_server=raw_input('smtp server: ')
to_addr =raw_input('to: ')
import smtplib
server = smtplib.SMTP(smtp_server,25)
server.set_debuglevel(1)
server.login(from_addr,password)
server.sendmail(from_addr,[to_addr],msg.as_string())
server.quit()
