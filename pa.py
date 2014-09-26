#!/usr/bin/python
#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import threading
import urllib
import urllib2
import httplib
import time
import cookielib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
 
class BlogRoobt():
    def __init__(self):
        self.urls=["http://blog.csdn.net/index.html"]
        self.threads=[]
        self.blogurl=[]
        self.lock=threading.Condition()
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(self.cj),
                )
        urllib2.install_opener(self.opener)
    def Post(self,url,data):
         try:
            postdata = urllib.urlencode(data)
            req = urllib2.Request(url, postdata)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            req.add_header('Accept','*/*')
            req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
            req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            req.add_header('Cache-Control', 'max-age=0')
            req.add_header('Connection', 'keep-alive')
            resp = urllib2.urlopen(req,postdata)
            return resp.read()
         except Exception,e:
            print "post error "+str(e)
            return None
    def Get(self,url):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
            req.add_header('Accept', '*/*')
            #req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
            req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            req.add_header('Connection', 'keep-alive')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            resp = urllib2.urlopen(req)
            return resp.read()
        except Exception,e:
            #print "get error "+str(e)
            return None
    def SendGet(self,url,data):
        try:
            postdata = urllib.urlencode(data)
            req = urllib2.Request(url+"?"+postdata)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
            req.add_header('Accept', '*/*')
            #req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
            req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            req.add_header('Connection', 'keep-alive')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            resp = urllib2.urlopen(req)
            return resp.read()
        except Exception,e:
            #print "get error "+str(e)
            return None
    def GetBlog(self,url):
        html=self.Get(url)
        if html==None:
            return False
        soup=BeautifulSoup(html)
        blog=soup.find("div",{"id":"article_details","class":"details"})
        title=blog.find("div","article_title").find("span",{"class":"link_title"}).text
        content=blog.find("div","article_content").encode("utf8")
        self.ProcessData(title,content)
        return True
    def Run(self):
        while True:
            if len(self.blogurl)==0:
                continue
            self.lock.acquire()
            url=self.blogurl.pop()
            print "---------",url
            self.lock.release()
            self.GetBlog(url)
            time.sleep(3)
    def Start(self):
        for url in self.urls:
            td=threading.Thread(target=self.PutBlogUrls,args=(url,))
            self.threads.append(td)
        run=threading.Thread(target=self.Run)
        self.threads.append(run)
        for i in self.threads:
            i.start()
        for i in self.threads:
            i.join()
    def PutBlogUrls(self,url):
        for i in range(1,20):
            nurl=url+"?page="+str(i)
            html=self.Get(nurl)
            if html==None:
                continue
            soup=BeautifulSoup(html)
            blogs=soup.find_all("div",{"class":"blog_list"})
            for b in blogs:
                try:
                    title=b.find("a",{"class":"category"}).find_next("a").text
                    href=b.find("a",{"class":"category"}).find_next("a")["href"]
                    #print href
                    #print title
                    #href=b.find("h1").find("a")["href"]
                    #title=b.find("h1").find("a").text
                except Exception,e:
                    continue
                self.lock.acquire()
                self.blogurl.append(href)
                self.lock.release()
            time.sleep(2) 
    def ProcessData(self,title,content):
        data={"title":title,"content":content}
        print self.Post("http://xxxxxx你自己网站的接受数据接口/api_blog",data)
blog=BlogRoobt()
blog.Start()
