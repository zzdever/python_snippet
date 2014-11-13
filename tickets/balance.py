# -*- coding: utf-8 -*-

import httplib, urllib, urllib2
import re
import os
import time
import random
import base64
import HTMLParser
import sys



userid = ''
params = ''
headers = {}
optionid = ''
votes = {
	'\xe9\x92\x9f\xe6\xb4\x81105\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':53, 'base':11546}, \
	'\xe6\xb1\xa4\xe9\x92\xa7\xe6\xb3\xa293\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':48, 'base':18115}, \
	'\xe5\x91\xa8\xe6\x81\xac\xe4\xbb\xaa75\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':54, 'base':10923}, \
	'\xe4\xbb\x9d\xe6\xb2\x90121\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':49, 'base':11200}, \
	'\xe5\xbc\xa0\xe5\x94\xaf47\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':51, 'base':11434}, \
	'\xe9\x83\x91\xe6\xb5\xb7\xe5\xbf\xa080\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':52, 'base':10933}, \
	'\xe6\x9c\xb1\xe7\xa2\xa7\xe9\x9b\xaf63\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':55, 'base':10902}, \
	'\xe8\x91\xa3\xe8\x8f\x81\xe8\x8f\x8165\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':47, 'base':10961}, \
	'\xe5\x90\xb4\xe8\x8e\x8e\xe8\x8e\x8e130\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':50, 'base':13208}, \
	'\xe9\x99\x88\xe6\xb3\xa2131\xe5\x8f\xb7': {'vote':'', 'rank':'', 'id':46, 'base':11007}}



def GenerateUser():
	global userid
	global params
	global headers

	res = base64.b64encode(str(random.randint(1234567, 9876543210000)))
	res = res.replace('=',chr(random.randint(ord('a'),ord('z'))))
	for i in range(random.randint(0,7)):
		j = random.randint(0,2)
		if j==0:
			res += str(i)
		elif j==1:
			res += chr(random.randint(ord('a'),ord('z')))
		else:
			res += chr(random.randint(ord('A'),ord('Z')))
	for i in range(random.randint(1,3)):
		pos = random.randint(0, res.__len__())
		res = res[:pos] + random.sample(['_', '-'], 1)[0] + res[pos:]

	userid = res

	params = urllib.urlencode({'userid':userid,      
                           'optionid':optionid});      

	headers = {"x-requested-with":"XMLHttpRequest", \
		"Content-Type":"application/x-www-form-urlencoded", \
		"Accept-Language":"en-US", \
		"Connection":"Keep-Alive", \
		#"Referer":"http://weixin.zdxsd900.com/zhandian/shangyu_dianshi/index.php?userid="+userid+"&optionid="+optionid, \
		"Accept":"*/*", \
		"Accept-Encoding":"gzip, deflate", \
		"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329 MicroMessenger/5.0.1" \
		};      



def main():
	GenerateUser()
	
	for i in range(10):
		conn = httplib.HTTPConnection("weixin.zdxsd900.com");      
	
		conn.request(method="POST",url="/zhandian/shangyu_dianshi/indexSave.php",body=params,headers=headers);      
	
		response = conn.getresponse();      
		tmp = response.read()
		result = tmp.split('|')[2]
		#print tmp
		if int(result) == 0:
			GenerateUser()
			continue
		print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), "id:%d result:%d user:%s" %(int(optionid), int(result), userid)
		
		conn.close();   
	
		t = random.randint(3,9)
		time.sleep(t/10.0)




def statics():
	global votes

	url = "http://weixin.zdxsd900.com/zhandian/shangyu_dianshi/index.php?userid=o"
	res = urllib2.urlopen(url)
	content = res.read()
	print content

	tagstack = []  
	key = ''
	class ShowStructure(HTMLParser.HTMLParser):  
		def handle_starttag(self, tag, attrs): tagstack.append(tag)  
		def handle_endtag(self, tag): tagstack.pop()  
		def handle_data(self, data):  
			global key
			if data.strip():  
				for tag in tagstack: 
					pass
					#sys.stdout.write('/'+tag) 
				#sys.stdout.write('%s\n' %data[:40].strip()) 
				if data[:40].strip().find('号')>=0:
					key = data[:40].strip()
				try:
					num = int(data[:40].strip())
				except Exception as e:
					return
				votes[key]['vote'] = num
	ShowStructure().feed(content)




def sort():
	for item in votes:
		sel = votes[item]['vote']
		rank = 0
		for j in votes:
			if int(votes[j]['vote']) > int(sel):
				rank += 1
		votes[item]['rank'] = rank

#for item in votes:
#	print item, votes[item]

while(1):
	vivi = '张唯47号'
	tmp = '周恬仪75号'
	k = vivi
	
	statics()
	sort()
	
	baseDiff = votes[k]['vote'] - votes[k]['base']
	item = random.choice(votes.keys())
	#while votes[item]['rank'] <= 4: # or int(votes[k]['vote'])>9500:
	while votes[item]['vote'] - votes[item]['base'] > baseDiff:
		#continue
		item = random.choice(votes.keys())
	optionid = str(votes[item]['id'])
	for ii in votes:
		print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), "id:%s" %ii, "status:", votes[ii]
	for i in range(random.randint(1,1)):
		main()

	continue
	t = random.randint(20,50)
	print 'sleep for %ds ...' %t
	time.sleep(t)
