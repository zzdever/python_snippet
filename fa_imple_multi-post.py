# -*- coding: utf-8 -*-

import httplib, urllib, urllib2
import re
import random
import sys
import types
import time
#from gevent import monkey
#monkey.patch_all()
#THREADS = 8


PRIMER_MIN_TM_LOWER = 50

PRIMER_MIN_TM = 57

PRIMER_PRODUCT_SIZE_RANGE_MIN = 400
PRIMER_PRODUCT_SIZE_RANGE_MAX = 550


requestString = ''

fields = []


boundary = ['---------------------------7430240943885405531850787391', 
            '---------------------------104589090111347224121624793124',
            '---------------------------5808774703469790281258421991',
            '---------------------------821511573972640848529211372',
            '---------------------------1485495501296289036508229237',
            '---------------------------105295072716776174091402991600']



def getFields():
    global fields
    
    PRIMER_PRODUCT_SIZE_RANGE = str(PRIMER_PRODUCT_SIZE_RANGE_MIN) + '-' + str(PRIMER_PRODUCT_SIZE_RANGE_MAX)
    
    
    fields = [
    ("PRIMER_TASK",'generic'),
    ("PRIMER_MISPRIMING_LIBRARY",'NONE'),
    ("SEQUENCE_TEMPLATE", requestString),
    ("MUST_XLATE_PRIMER_PICK_LEFT_PRIMER",1),
    ("MUST_XLATE_PRIMER_PICK_RIGHT_PRIMER",1),
    ("SEQUENCE_PRIMER",''),
    ("SEQUENCE_INTERNAL_OLIGO",''),
    ("SEQUENCE_PRIMER_REVCOMP",''),
    ("SEQUENCE_ID",''),
    ("SEQUENCE_TARGET",''),
    ("SEQUENCE_OVERLAP_JUNCTION_LIST",''),
    ("SEQUENCE_EXCLUDED_REGION",''),
    ("SEQUENCE_PRIMER_PAIR_OK_REGION_LIST",''),
    ("SEQUENCE_INCLUDED_REGION",''),
    ("SEQUENCE_START_CODON_POSITION",''),
    ("SEQUENCE_INTERNAL_EXCLUDED_REGION",''),
    ("SEQUENCE_FORCE_LEFT_START",-1000000),
    ("SEQUENCE_FORCE_RIGHT_START",-1000000),
    ("SEQUENCE_FORCE_LEFT_END",-1000000),
    ("SEQUENCE_FORCE_RIGHT_END",-1000000),
    ("SEQUENCE_QUALITY",''),
    ("PRIMER_MIN_QUALITY",0),
    ("PRIMER_MIN_END_QUALITY",0),
    ("PRIMER_QUALITY_RANGE_MIN",0),
    ("PRIMER_QUALITY_RANGE_MAX",100),
    ("Pick Primers",'Pick Primers'),
    #("Upload", 'filename=""\r\nContent-Type: application/octet-stream\r\n'),
    ("PRIMER_MIN_SIZE",19),
    ("PRIMER_OPT_SIZE",20),
    ("PRIMER_MAX_SIZE",23),
    ("PRIMER_MIN_TM",PRIMER_MIN_TM),
    ("PRIMER_OPT_TM",59.0),
    ("PRIMER_MAX_TM",62.0),
    ("PRIMER_PAIR_MAX_DIFF_TM",5.0),
    ("PRIMER_TM_FORMULA",1),
    ("PRIMER_PRODUCT_MIN_TM",-1000000.0),
    ("PRIMER_PRODUCT_OPT_TM",0.0),
    ("PRIMER_PRODUCT_MAX_TM",1000000.0),
    ("PRIMER_MIN_GC",30.0),
    ("PRIMER_OPT_GC_PERCENT",50.0),
    ("PRIMER_MAX_GC",70.0),
    ("PRIMER_PRODUCT_SIZE_RANGE",PRIMER_PRODUCT_SIZE_RANGE),
    ("PRIMER_NUM_RETURN",5),
    ("PRIMER_MAX_END_STABILITY",9.0),
    ("PRIMER_MAX_LIBRARY_MISPRIMING",12.00),
    ("PRIMER_PAIR_MAX_LIBRARY_MISPRIMING",20.00),
    ("MUST_XLATE_PRIMER_THERMODYNAMIC_OLIGO_ALIGNMENT",1),
    ("PRIMER_MAX_TEMPLATE_MISPRIMING_TH",40.00),
    ("PRIMER_PAIR_MAX_TEMPLATE_MISPRIMING_TH",70.00),
    ("PRIMER_MAX_SELF_ANY_TH",45.0),
    ("PRIMER_MAX_SELF_END_TH",35.0),
    ("PRIMER_PAIR_MAX_COMPL_ANY_TH",45.0),
    ("PRIMER_PAIR_MAX_COMPL_END_TH",35.0),
    ("PRIMER_MAX_HAIRPIN_TH",24.0),
    ("PRIMER_MAX_TEMPLATE_MISPRIMING",12.00),
    ("PRIMER_PAIR_MAX_TEMPLATE_MISPRIMING",24.00),
    ("PRIMER_MAX_SELF_ANY",8.00),
    ("PRIMER_MAX_SELF_END",3.00),
    ("PRIMER_PAIR_MAX_COMPL_ANY",8.00),
    ("PRIMER_PAIR_MAX_COMPL_END",3.00),
    ("PRIMER_MAX_NS_ACCEPTED",0),
    ("PRIMER_MAX_POLY_X",4),
    ("PRIMER_INSIDE_PENALTY",-1.0),
    ("PRIMER_OUTSIDE_PENALTY",0),
    ("PRIMER_FIRST_BASE_INDEX",1),
    ("PRIMER_GC_CLAMP",0),
    ("PRIMER_MAX_END_GC",5),
    ("PRIMER_MIN_LEFT_THREE_PRIME_DISTANCE",3),
    ("PRIMER_MIN_RIGHT_THREE_PRIME_DISTANCE",3),
    ("PRIMER_MIN_5_PRIME_OVERLAP_OF_JUNCTION",7),
    ("PRIMER_MIN_3_PRIME_OVERLAP_OF_JUNCTION",4),
    ("PRIMER_SALT_MONOVALENT",50.0),
    ("PRIMER_SALT_CORRECTIONS",1),
    ("PRIMER_SALT_DIVALENT",1.5),
    ("PRIMER_DNTP_CONC",0.6),
    ("PRIMER_DNA_CONC",50.0),
    ("PRIMER_SEQUENCING_SPACING",500),
    ("PRIMER_SEQUENCING_INTERVAL",250),
    ("PRIMER_SEQUENCING_LEAD",50),
    ("PRIMER_SEQUENCING_ACCURACY",20),
    ("MUST_XLATE_PRIMER_LIBERAL_BASE",1),
    ("MUST_XLATE_PRIMER_PICK_ANYWAY",1),
    ("MUST_XLATE_PRIMER_EXPLAIN_FLAG",1),
    ("PRIMER_WT_SIZE_LT",1.0),
    ("PRIMER_WT_SIZE_GT",1.0),
    ("PRIMER_WT_TM_LT",1.0),
    ("PRIMER_WT_TM_GT",1.0),
    ("PRIMER_WT_GC_PERCENT_LT",0.0),
    ("PRIMER_WT_GC_PERCENT_GT",0.0),
    ("PRIMER_WT_SELF_ANY_TH",0.0),
    ("PRIMER_WT_SELF_END_TH",0.0),
    ("PRIMER_WT_HAIRPIN_TH",0.0),
    ("PRIMER_WT_TEMPLATE_MISPRIMING_TH",0.0),
    ("PRIMER_WT_SELF_ANY",0.0),
    ("PRIMER_WT_SELF_END",0.0),
    ("PRIMER_WT_TEMPLATE_MISPRIMING",0.0),
    ("PRIMER_WT_NUM_NS",0.0),
    ("PRIMER_WT_LIBRARY_MISPRIMING",0.0),
    ("PRIMER_WT_SEQ_QUAL",0.0),
    ("PRIMER_WT_END_QUAL",0.0),
    ("PRIMER_WT_POS_PENALTY",0.0),
    ("PRIMER_WT_END_STABILITY",0.0),
    ("PRIMER_PAIR_WT_PRODUCT_SIZE_LT",0.0),
    ("PRIMER_PAIR_WT_PRODUCT_SIZE_GT",0.0),
    ("PRIMER_PAIR_WT_PRODUCT_TM_LT",0.0),
    ("PRIMER_PAIR_WT_PRODUCT_TM_GT",0.0),
    ("PRIMER_PAIR_WT_COMPL_ANY_TH",0.0),
    ("PRIMER_PAIR_WT_COMPL_END_TH",0.0),
    ("PRIMER_PAIR_WT_TEMPLATE_MISPRIMING_TH",0.0),
    ("PRIMER_PAIR_WT_COMPL_ANY",0.0),
    ("PRIMER_PAIR_WT_COMPL_END",0.0),
    ("PRIMER_PAIR_WT_TEMPLATE_MISPRIMING",0.0),
    ("PRIMER_PAIR_WT_DIFF_TM",0.0),
    ("PRIMER_PAIR_WT_LIBRARY_MISPRIMING",0.0),
    ("PRIMER_PAIR_WT_PR_PENALTY",1.0),
    ("PRIMER_PAIR_WT_IO_PENALTY",0.0),
    ("PRIMER_INTERNAL_MIN_SIZE",18),
    ("PRIMER_INTERNAL_OPT_SIZE",20),
    ("PRIMER_INTERNAL_MAX_SIZE",27),
    ("PRIMER_INTERNAL_MIN_TM",57.0),
    ("PRIMER_INTERNAL_OPT_TM",60.0),
    ("PRIMER_INTERNAL_MAX_TM",63.0),
    ("PRIMER_INTERNAL_MIN_GC",20.0),
    ("PRIMER_INTERNAL_OPT_GC_PERCENT",50.0),
    ("PRIMER_INTERNAL_MAX_GC",80.0),
    ("PRIMER_INTERNAL_MAX_SELF_ANY_TH",47.00),
    ("PRIMER_INTERNAL_MAX_SELF_END_TH",47.00),
    ("PRIMER_INTERNAL_MAX_HAIRPIN_TH",47.00),
    ("PRIMER_INTERNAL_MAX_SELF_ANY",12.00),
    ("PRIMER_INTERNAL_MAX_SELF_END",12.00),
    ("PRIMER_INTERNAL_MIN_QUALITY",0),
    ("PRIMER_INTERNAL_MAX_NS_ACCEPTED",0),
    ("PRIMER_INTERNAL_MAX_POLY_X",5),
    ("PRIMER_INTERNAL_MISHYB_LIBRARY",'NONE'),
    ("PRIMER_INTERNAL_MAX_LIBRARY_MISHYB",12.00),
    ("PRIMER_INTERNAL_SALT_MONOVALENT",50.0),
    ("PRIMER_INTERNAL_DNA_CONC",50.0),
    ("PRIMER_INTERNAL_SALT_DIVALENT",1.5),
    ("PRIMER_INTERNAL_DNTP_CONC",0.0),
    ("PRIMER_INTERNAL_WT_SIZE_LT",1.0),
    ("PRIMER_INTERNAL_WT_SIZE_GT",1.0),
    ("PRIMER_INTERNAL_WT_TM_LT",1.0),
    ("PRIMER_INTERNAL_WT_TM_GT",1.0),
    ("PRIMER_INTERNAL_WT_GC_PERCENT_LT",0.0),
    ("PRIMER_INTERNAL_WT_GC_PERCENT_GT",0.0),
    ("PRIMER_INTERNAL_WT_SELF_ANY_TH",0.0),
    ("PRIMER_INTERNAL_WT_SELF_END_TH",0.0),
    ("PRIMER_INTERNAL_WT_HAIRPIN_TH",0.0),
    ("PRIMER_INTERNAL_WT_SELF_ANY",0.0),
    ("PRIMER_INTERNAL_WT_SELF_END",0.0),
    ("PRIMER_INTERNAL_WT_NUM_NS",0.0),
    ("PRIMER_INTERNAL_WT_LIBRARY_MISHYB",0.0),
    ("PRIMER_INTERNAL_WT_SEQ_QUAL",0.0),
    ("PRIMER_INTERNAL_WT_END_QUAL",0.0)
    ]
    
    return fields


body = ''
content_type = ''

def encode_multipart_formdata(fields): 
    global body
    global content_type
    global boundary
        
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filepath) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """ 
    #BOUNDARY = mimetools.choose_boundary() 
    BOUNDARY = boundary[random.randint(0, len(boundary)-1)]
    CRLF = '\r\n' 
    L = [] 
    for (key, value) in fields: 
        if type(value)!=types.StringType:
            value = str(value)
        L.append('--' + BOUNDARY) 
        L.append('Content-Disposition: form-data; name="%s"' % key) 
        L.append('') 
        L.append(value) 
        
    '''
    for (key, filepath) in files: 
        L.append('--' + BOUNDARY) 
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, os.path.basename(filepath))) 
        L.append('Content-Type: %s' % get_content_type(filepath)) 
        L.append('') 
        L.append(open(filepath, 'rb').read()) 
    '''
    L.append('--' + BOUNDARY + '--') 
    L.append('') 
    
    body = CRLF.join(L)
    #print body 
    
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY 
    
    
def request():
    print fields
    encode_multipart_formdata(fields)
    headers = {
        'Host': 'primer3.ut.ee', \
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0', \
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', \
        'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3', \
        'Accept-Encoding': 'gzip, deflate', \
        'DNT': '1', \
        'Referer': 'http://primer3.ut.ee/', \
        'Connection': 'keep-alive', \
        'Content-Type': content_type
    }
    
    
    result = ''
    trytimes = 0
    while True:
        try:
            conn = httplib.HTTPConnection("primer3.ut.ee", timeout = 3)
            conn.request(method="POST",url="/cgi-bin/primer3/primer3web_results.cgi",body=body,headers=headers);      
            response = conn.getresponse();
            result = response.read()
        except Exception,e:
            print e,'connection error, try again'
            trytimes = trytimes + 1
            if trytimes>7:
                break
            continue
        else:
            break
        

    

    #conn = httplib.HTTPConnection("primer3.ut.ee");      
    #conn.request(method="POST",url="/cgi-bin/primer3/primer3web_results.cgi",body=body,headers=headers);      
    #response = conn.getresponse(); 
    #result = response.read()

    if result.find('NO PRIMERS FOUND') >= 0:
        print 'NO PRIMERS FOUND'
        print requestString
        return ''
    elif result.find('OLIGO') >= 0:
        info = re.findall('OLIGO[\s\S]+TARGETS', result)
        if len(info)>0:
            info = info[0]
        starttags = re.findall('<a href="primer3web_help.cgi#[^>]+>', info)
        for starttag in starttags:
            info = info.replace(starttag, '')
        endtags = re.findall('</a>', info)
        for endtag in endtags:
            info = info.replace(endtag, '')
        
        #print info
        return info
    else:
        print 'unknown result'
        try:
            print result
        except Exception,e:
            print e
        return ''

    conn.close(); 


def requestDriver():
    global PRIMER_MIN_TM
    global PRIMER_PRODUCT_SIZE_RANGE_MIN
    
    result = ''
    for PRIMER_PRODUCT_SIZE_RANGE_MIN in [400,450]:
        PRIMER_MIN_TM = 57
        while PRIMER_MIN_TM>PRIMER_MIN_TM_LOWER:
            print 'trying',PRIMER_PRODUCT_SIZE_RANGE_MIN,PRIMER_MIN_TM
            getFields()
            res = request()
            if len(res)>0:
                result = res
                break
            else:
                PRIMER_MIN_TM = PRIMER_MIN_TM - 1
                if PRIMER_MIN_TM<=PRIMER_MIN_TM_LOWER:
                    return 'NO PRIMERS FOUND even under condition '+str(PRIMER_MIN_TM+1)+' 400-550'
    
    if len(result)>0:
        return result
    else:
        return ''
    
    
    
    

if len(sys.argv)<2:
    filename = 'fa.txt'
    print 'You can indicate the filename by typing:\npython fa.py <filename>'  
    print 'filename set to default: fa.txt'
else:
    filename = sys.argv[1]
    
time.sleep(3)
f = open(filename, 'r')
lines = f.readlines()
f.close()
index = 0

fileResult = 'fa_result.txt'
fr = open(fileResult, 'w')
fr.close()
fileError = 'fa_error.txt'
fe = open(fileError, 'w')
fe.close()
for index in range(len(lines)):
    if lines[index].find('>')>=0:
        requestString = lines[index].strip() + '\r\n' + lines[index+1].strip()
        print requestString
        res = requestDriver()
        
        if len(res)>0:
            if res.find('NO PRIMERS FOUND')>=0:
                filetowrite = fileError
            else:
                filetowrite = fileResult
        else:
            res = 'error in request, connection error/time out, or error in input'
            filetowrite = fileError
                        
        print res
        f = open(filetowrite, 'a')
        f.write(lines[index].strip())
        f.write('\n'+lines[index+1].strip())
        f.write('\n\n'+res+'\n\n')    
        f.close()
        
        index = index + 2
        

    