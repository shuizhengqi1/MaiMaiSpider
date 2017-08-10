#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/8 下午2:28
# @Author  : yanghengxing
# @Email   : yanghengxing@idcos.com
# @File    : Main.py
import BeautifulSoup
import requests
import json
import time
from threading import Thread
from Queue import Queue
from db import mmidredis
from UserInfo import User

headers=[]
queue = []
mmid = []
jobquene = Queue()
listquene = Queue(maxsize=10)
def user(encode_mmid):
  try:
    url = 'https://maimai.cn/contact/comment_list/'+encode_mmid+'?jsononly=1'
    rsq = requests.get(url,headers=header).content
    js = json.loads(rsq,encoding='utf-8')
    data = js['data']['card']
    User(data).insert()
  except:
        try:
            url = 'https://maimai.cn/contact/interest_contact/'+encode_mmid+'?jsononly=1'
            req = requests.get(url, headers=header).content
            js1 = json.loads(req, encoding='utf-8')
            data1 = js1['data']
            for sdata in data1:
                User(sdata['card']).insert()
        except:
            pass

def getURl(encodemmid):
  while True:
   try:
    if listquene.empty():
        url = 'https://maimai.cn/contact/interest_contact/'+encodemmid+'?jsononly=1'
        rsq = requests.get(url, headers=header).content
        js = json.loads(rsq, encoding='utf-8')
        data = js['data']
        for sdata in data:
            if sdata['card']['mmid'] not in mmid:
                a = sdata['card']['encode_mmid']
                # print a
                mmid.append(sdata['card']['mmid'])
                jobquene.put(a)
                # time.sleep(1)
                listquene.put(a)
    else:
        encode_mmid = listquene.get()
        getURl(encode_mmid)
   except:
       time.sleep(1)
def work():
    while True:
      # print mmid
      if not jobquene.empty():
        encode_mmid = jobquene.get()
        user(encode_mmid)
        jobquene.task_done()


#TODO 目前连接访问出现问题，待解决

def workGetUrl():
    if mmid == []:
        getURl('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoxNDkwMDcxLCJ0IjoiY3R0IiwibGV2ZWwiOjF9.KuTVsccej6dODRYufcs1LD7DnX8hMyGfdGOK0kKfhGQ')

t1 = Thread(target=workGetUrl)
t1.start()
for i in range(50):
    t = Thread(target=work())
    t.setDaemon(True)
    t.start()

