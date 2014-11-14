import urllib2
import urllib
import re
import sys


f = open('/Users/ying/iii.html', 'r')
lines = f.readlines()
urls = []
for line in lines:
    line = re.findall('"(https://[^"]+)"', line)[0]
    urls.append(line)
    

print len(urls)
sys.exit(0)
for i in range(43,len(urls)):

    url = urls[i]

    res = urllib2.urlopen(url)
    header = res.headers
    name = re.findall('filename="([^"]+)"',header['content-disposition'])
    
    if len(name)>0:
        name = name[0]
    else:
        print i,'fail to get name'
        continue
        
    print name
    fname = urllib.unquote(name).decode('utf-8')
    fname = fname.replace('/',' ')
    fname = fname.replace('\\',' ')
    fname = fname.replace(':','_')
    print fname
    
    
    #sys.exit(0)

    f=open(fname,'wb')

    data = res.read()
    f.write(data)
    f.close()
    print i,'done'