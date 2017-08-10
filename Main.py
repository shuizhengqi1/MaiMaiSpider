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
header = {'cookie':'seid=s1502241961732; guid=GxsfBBsTGAQYGAQbGBxWBxgbHhgYGh8ZHxtWHBkEHRkfBUNYS0xLeQoaEwQYGxsZBBoEGhwFT0dFWEJpCgNFQUlPbQpPQUNGCgZmZ35iYQIKHBkEHRkfBV5DYUhPfU9GWlprCgMcdRgbdRobCnIKeWUKSUtnCkZPXkRjChFCWUVeRENJS2cCChoEHwVLRkZDUEVn; koa:sess=eyJ1IjoiMzg1NzE2ODEiLCJzZWNyZXQiOiJ0bU9MTjVxckZtZ3pEWThiUkVMN1ZKMzIiLCJtaWQ0NTY4NzYwIjpmYWxzZSwic3RhdHVzIjp0cnVlLCJfZXhwaXJlIjoxNTAyMzI4NzE0MTgwLCJfbWF4QWdlIjo4NjQwMDAwMH0=; koa:sess.sig=tNhDS6Oilu4N335demLz9vyfXsA; token="NEO7dpqYIh2ZJtXeiF/s4yofvew7csuK9pGfs8rHNLHcf6MZCV5+dEsWHXTNc6nN8CKuzcDfAvoCmBm7+jVysA=="; sessionid=fa757ce58f1d331dbde2ca902b37029e; uid="gF2B3R3Jh2IUTUBxcia+vPAirs3A3wL6ApgZu/o1crA="',
           'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
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

