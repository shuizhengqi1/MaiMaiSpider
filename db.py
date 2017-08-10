#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/9 下午4:47
# @Author  : yanghengxing
# @Email   : yanghengxing@idcos.com
# @File    : db.py
import sqlite3
import redis
class infodb:
    # con = sqlite3.connect('userinfo.db')
    # c = con.cursor()
    # c.execute('''CREATE TABLE  IF NOT EXISTS USERINFO(
    #                     MMID INT PRIMARY KEY NOT NULL,
    #                     DIST INT NOT NULL,
    #                     NAME VARCHAR(100) NOT NULL,
    #                     RANK INT NOT NULL ,
    #                     POSITION VARCHAR(50) NOT NULL,
    #                     COMPANY VARCHAR(50) NOT NULL,
    #                     SCHOOLS VARCHAR(50) NOT NULL,
    #                     CITY VARCHAR(50) NOT NULL ,
    #                     PROVINCE VARCHAR(50) NOT NULL )
    #                     ''')
    # c.close()
    def insertData(self,mmid,dist,name,rank,position,company,schools,city,province):
      try:
        con = sqlite3.connect('userinfo.db')
        c = con.cursor()
        sql = '''insert into USERINFO VALUES(%s,%s,'%s',%s,'%s','%s','%s','%s','%s')'''%(mmid,dist,name,rank,position,company,schools,city,province)
        print sql
        c.execute(sql)
        con.commit()
        c.close()
        con.close()
      except:
          print 'same mmid '

class mmidredis:
    redispool = redis.ConnectionPool(host='localhost',port=6379)
    def setKey(self,key):
        r = redis.Redis(connection_pool=self.redispool)
        r.set(key,'1')