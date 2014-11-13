# -*- coding: utf-8 -*-

import httplib, urllib2
import re
import os
import HTMLParser
import sys
import hashlib
import xlrd

def readXls():
	months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',\
		7: 'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
	filename = 'input.xls'
	file = xlrd.open_workbook(filename)
	sheet = file.sheet_by_index(1)
	
	data = []
	for i in range(sheet.nrows):
		value = sheet.cell_value(i,2)
		year = int(value/10000)
		month = int(value/100) - year*100
		month = months[month]		
		year = str(year)
		date = int(value%100)
		if date in range(1,10):
			date = '0'+str(date)
		else:
			date = str(date)
		
		data.append(date+'-'+month+'-'+year)

	'''
	for item in data:
		print item
	print len(data)
	'''
	
	return data
	

def buildUrl(direction, date, hour):
	up = '50' # +:N  -:S
	down = '10'
	left = '110' # +:E -:W
	right = '140'
	
	'''
	day = '26'
	month = 'Jul'
	year = '2009'
	''' 
	day, month, year = date.split('-')

	url = 'http://apdrc.soest.hawaii.edu/las/ProductServer.do?xml=%3C%3Fxml+version%3D%221.0%22%3F%3E%3ClasRequest+package%3D%22%22+href%3D%22file%3Alas.xml%22+%3E%3Clink+match%3D%22%2Flasdata%2Foperations%2Foperation[%40ID%3D%27Data_Extract%27]%22+%2F%3E%3Cproperties+%3E%3Cferret+%3E%3Cview+%3Exy%3C%2Fview%3E%3Cformat+%3Etxt%3C%2Fformat%3E%3Cexpression+%3E%3C%2Fexpression%3E%3Cinterpolate_data+%3Efalse%3C%2Finterpolate_data%3E%3C%2Fferret%3E%3C%2Fproperties%3E%3Cargs+%3E%3Clink+match%3D%22%2Flasdata%2Fdatasets%2Fccmp_6hourly%2Fvariables%2F'+direction+'-ccmp_6hourly%22+%2F%3E%3Cregion+%3E%3Crange+low%3D%22'+left+'%22+type%3D%22x%22+high%3D%22'+right+'%22+%2F%3E%3Crange+low%3D%22'+down+'%22+type%3D%22y%22+high%3D%22'+up+'%22+%2F%3E%3Cpoint+v%3D%22'+day+'-'+month+'-'+year+'+'+hour+'%3A00%3A00%22+type%3D%22t%22+%2F%3E%3C%2Fregion%3E%3C%2Fargs%3E%3C%2FlasRequest%3E&JSESSIONID=692DCBE0E3CD32D12DA2D08A23209742'
	
	return url


dateset = readXls()

amount = 0
for item in dateset:
	for direction in ['u', 'v']:
		for hour in ['00','06','12','18']:
			amount = amount + 1
			#filename = 'apdrc-data/'+hashlib.sha1(url2).hexdigest()+'.txt'
			filename = 'apdrc-data/'+item.upper()+' '+hour+'00-'+direction.upper()+'.txt'
			if os.path.exists(filename):
				print filename, 'done', '%.2f%%' %(100.0*amount/(len(dateset)*2*4))
				continue

			url = buildUrl(direction,item,hour)
			request = urllib2.urlopen(url)
			response = request.read()
			
			url2 = re.findall(r'"\S+apdrc\S+"', response)[0].strip('"')
			
			request = urllib2.urlopen(url2)
			response = request.read()
			
			if not os.path.exists('apdrc-data/'):
				os.mkdir('apdrc-data')
			
			with open(filename, 'w') as f:
				f.write(response)
				f.close()
			print filename, 'done', '%.2f%%' %(100.0*amount/len(dateset)/8)
