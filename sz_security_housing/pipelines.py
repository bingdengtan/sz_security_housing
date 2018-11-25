# -*- coding: utf-8 -*-

from urllib import request
from lxml import etree
from sz_security_housing.db import Mysql
from sz_security_housing.sqlMapping import MonthlySqlMapping as mSql
from sz_security_housing.sqlMapping import TodaySqlMapping as tSql
import re

class SzSecurityHousingPipeline(object):
	def process_item(self, item, spider):
		# print(item)
		url='http://bzflh.szjs.gov.cn/TylhW/lhmcAction.do?method=queryDetailLhc&lhmcId=%s&waittype=2'%(item['userid'])
		# print(url)
		try:
			response = request.urlopen(url,timeout=5)
			page = response.read()
			page = page.decode('utf-8')
			selector = etree.HTML(page)
			content=selector.xpath('//div[@class="leader_intro1"]')[1].xpath('string(.)')
			place = re.search('户籍所在区.*区',content).group().replace('户籍所在区：','')
			item['place']=place
			num=len(selector.xpath('//div[@class="leader_intro1"]'))-1
			item['num']=num
		except Exception:
			print ("Error:%s"%(item['seqno']))
		else:	
			print ("Success:%s"%(item['seqno']))

		mysql = Mysql()
		sql = tSql['insert']
		result = mysql.insertOne(sql, (item['userid'], item['creditId'], item['name'], item['seqno'], item['applyNo'], item['num'], item['place']))
		mysql.end()
		# ret=str(item['userid'])+','+str(item['seqno'])+","+str(item['applyNo'])+","+str(item['num'])+","+str(item['place'])+"\n"
		# saveFile = open('data.txt','a')  
		# saveFile.write(ret)  
		# saveFile.close()  
		# print(item)