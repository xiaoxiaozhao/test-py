#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import re
def search(s,path='/home/xz'):
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path,i)):
            search(s,os.path.join(path,i))
        if os.path.isfile(os.path.join(path,i)) and re.search(s,os.path.join(path,i)):
            print os.path.join(path,i)
if __name__=="__main__":
    search("txt")
            
        
