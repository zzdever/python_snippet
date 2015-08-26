# -*- coding: utf-8 -*-

# This script reply a post with floor number and email hashed with sha1
#
# The input is a text file naming 'userinfo'
# in which contains three lines
# and they are username, email and password respectively
#

import hashlib
import urllib
import urllib2
import cookielib
#import CookieJar
import bs4
import re
import lxml

# pack as a class
class cc98():
        # initialize
	def __init__(self, name, pwd):
		self.name = name
		self.pwd = pwd = hashlib.md5(pwd).hexdigest()
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

	def login(self):
		params = {
				'a':'i',
				'u':self.name,
				'p':self.pwd,
				'userhidden':1
		}

		data = urllib.urlencode(params)
		LogUrl = "http://www.cc98.org/sign.asp"
		try:
			req = urllib2.Request(LogUrl, data)
		except:
			print "Request Error!"
			print req

		try:
			response = self.opener.open(req)
		except:
			print "Open Error!"
			print response

        # get info
        def info(self, url):
            soup = bs4.BeautifulSoup(self.opener.open(url).read(), 'lxml')
            keys = ('RootID', 'followup', 'UserName', 'passwd', 'star', 'signflag')
            d = {}
            for key in keys:
                soupres = soup.find(attrs={'name': key})
                #print soupres
                if soupres is not None:
                        d[key] = soupres['value']
            #d = {key: soup.find(attrs={'name': key})['value'] for key in keys}
            d['method'] = 'fastreply'
            d['Expression'] = 'face7.gif'
            d['BoardID'] = re.search(r'BoardID=(\d+)', soup.find(attrs={'name': 'frmAnnounce'})['action']).group(1)
            return d

        '''
        def floor(self, url):
                soup = bs4.BeautifulSoup(self.opener.open(url).read(), 'lxml')
                soupres = soup.findAll(attrs={'name': re.compile(r'reply\d+')})
                fl = 0
                for item in soupres:
                        print item
                        #print type(item['id'])
                        num = int(re.match(r'reply(\d+)', item['id']).group(1))
                        if num > fl:
                                fl = num
                return fl
        '''
            
        def reply(self, url, content):
            d = self.info(url)
            d['Content'] = content
            data = self.opener.open(urllib2.Request(
                reply_url, 
                headers={'Referer': 'http://www.cc98.org'}, 
                data=urllib.urlencode(d)
            )).read()
            return re.search('成功', data) is not None

reply_url = 'http://www.cc98.org/SaveReAnnounce.asp'

with open('userinfo') as f:
         # read in information
         name = f.readline().strip()
         mail = f.readline().strip()
         password = f.readline().strip()

         url = "http://www.cc98.org/dispbbs.asp?boardID=509&ID=4222721&page=1"
         #cc = cc98(name, password)
         #cc.login()  # log in first
         # get total post number to calculate floor number
         data = urllib2.urlopen(url).read().decode('utf-8')
         reres = re.search(r'本主题贴数\s*<b>(\d+)</b>'.decode('utf-8'), data)
         if reres is not None:
                 floor = reres.group(1)
         #response = cc.opener.open(url)
         cc.reply(url, str(int(floor)+1)+' '+hashlib.sha1(mail).hexdigest())


	
