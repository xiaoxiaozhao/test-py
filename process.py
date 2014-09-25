#!/usr/bin/python
#-*- coding=utf8 -*-
import os
print 'process(%s) start...' %os.getpid()
pid=os.fork()
if pid==0:
    print 'it is a child process(%s) and my parent is %s' %(os.getpid(),os.getppid())
else:
    print '(%s) just create a child process(%s)' %(os.getpid(),pid)
