# coding: utf-8

import urllib2
import urllib
from HTMLParser import HTMLParser
import re
from bs4 import BeautifulSoup 
import sys
import os
import gevent
from gevent import monkey
monkey.patch_all()


TOTAL_THREAD = 7

cid = 2600
cidWriteFlag = 0

root = 'stampDB'
if os.path.exists(root)==False:
    os.mkdir(root)

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.linksre = set([])
        self.info = ''
        # flags
        self.flag = 0   #li tag
        self.infoStartFlag = 0  
        self.xxjsFlag = 0
        self.xxjsStackCnt = 0
        self.imgFlag = 0
                
    def handle_starttag(self, tag, attrs):
		#print "Encountered the beginning of a %s tag" % tag            
        if tag == "li":
            if len(attrs)>0:
                condition = ['onclick' in item for item in attrs]
                if True in condition:
                    self.infoStartFlag = 1
                    for (var,val) in attrs:
                        val = val.decode('utf-8')
                        if not val.find('attachment')<0:
                            links = re.findall('attach[^,]+.jpg', val)
                        else: continue
                        for item in links:
                            self.linksre.add(item)
            elif len(attrs)==0:
                self.flag = 1
                
        if tag == "div":
            if (u'class',u'xxjs') in attrs:
                self.xxjsFlag = 1
                self.info = self.info + u'\n\n详细介绍：\n'
            else:
                if self.xxjsFlag == 1:
                    self.xxjsStackCnt = self.xxjsStackCnt + 1
                    
        if tag == "img":
            if self.xxjsFlag == 1:
                for (var,val) in attrs:
                    if var == u'src':
                        self.info = self.info + '\n<img>' + val + '</img>\n'
                
                            
    def handle_data(self, data):
        if self.infoStartFlag == 1 and self.flag == 1:
            self.info = self.info + data
        
        if self.xxjsFlag == 1:
            self.info = self.info + data
            
    def handle_endtag(self, tag):
        if tag == 'li' and self.infoStartFlag == 1 and self.flag == 1:
            self.info = self.info + '\n'
            self.flag = 0
        if tag == 'div' and self.xxjsFlag == 1:
            self.xxjsStackCnt = self.xxjsStackCnt - 1
            if self.xxjsStackCnt < 0:
                self.xxjsFlag = 0



def grasp():
    global cid
    global cidWriteFlag
    
    while True:
        if cidWriteFlag == 1:
            gevent.sleep(1.0/1000)
        else:
            cidWriteFlag = 1
            cidLocal = cid
            url = 'http://www.chinau.cc/cata/detail?cid='+str(cid)
            cid = cid + 1
            cidWriteFlag = 0
            print 'start: ', url
            break
    
    tryTime = 3
    while True:
        try:    
            request = urllib2.urlopen(url)
        except Exception,e:
            print cidLocal, 'error:', e
            tryTime = tryTime - 1
            if tryTime<=0:
                return cidLocal
        else:
            data = request.read()
            break
    
    dire = re.findall('<title>([\S\s]+)- 中国邮票目录 - 邮票价格表 - 邮票历史价格 - 来邮来邮集邮网集邮吧</title>', data)
    if len(dire)<1:
        print 'directory set to default'
        dire = '['+str(cidLocal)+']'
    else:
        dire = '['+str(cidLocal)+']'+dire[0].strip().replace(' ', '-')
    
    hp = MyHTMLParser()
    hp.info = url
    hp.feed(data.decode('utf-8'))
    hp.close()
    #print hp.info.strip()

    if os.path.exists(os.path.join(root,dire))==False:
        os.mkdir(os.path.join(root,dire))
    else:
        ls = os.listdir(os.path.join(root,dire))
        lss = []
        for item in ls:
            if item.find('.jpg')>=0:
                lss.append(item)
        if len(lss) >= len(hp.linksre):
            print 'skip: ', url
            return 0
    
    with open(os.path.join(root,dire,'info.txt'), 'w') as f:
        f.write(hp.info.encode('utf-8'))
        f.close()
        
    for item in hp.linksre:
        tmp = re.findall('t(\d+).jpg', item)
        if len(tmp)>0:
            tmp = int(tmp[0])
            url = 'http://www.chinau.cc/'+item
            data = urllib.urlopen(url).read()
            while True:
                filename = url.split('/')[-1]
                url2 = url.replace('t'+str(tmp)+'.jpg','t'+str(tmp+1)+'.jpg')
                while True:
                    try:
                        data2 = urllib.urlopen(url2).read()
                    except Exception,e:
                        print 'error: ',url2, e
                        gevent.sleep(1)
                        continue
                    else:
                        break
                if data2.find('404 Page Not Found') >= 0:
                    url2 = url2 = url.replace('t'+str(tmp)+'.jpg','t5.jpg')
                    url2 = url2.replace('attachment','attachment/o')
                    while True:
                        try:
                            data2 = urllib.urlopen(url2).read()
                        except Exception,e:
                            print 'error: ',url2, e
                            gevent.sleep(1)
                            continue
                        else:
                            break
                    if data2.find('404 Page Not Found') >= 0:
                        filename = str(filename)
                        with open(os.path.join(root,dire,filename), 'wb') as f:
                            f.write(data)
                            f.close()
                        print url, 'done'
                        break
                    else:
                        filename = str(url2.split('/')[-1])
                        with open(os.path.join(root,dire,filename), 'wb') as f:
                            f.write(data2)
                            f.close()
                        print url2, 'done'
                        break
                else:
                    data = data2
                    tmp = tmp + 1
                    url = url2
        else:
            print 'error with',item
    
    return 0
        

def driver(pid):
    failCnt = 0 
    while True:
        try:
            res = grasp()
            if res > 0:
                print res, 'error'
                failCnt = failCnt + 1
                if failCnt > 20:
                    print 'thread', pid, 'done'
                    return 
        except Exception,e:
            print e



threads = [gevent.spawn(driver, i) for i in range(TOTAL_THREAD)]
gevent.joinall(threads) 
gevent.wait()  




