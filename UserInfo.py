#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/9 下午4:25
# @Author  : yanghengxing
# @Email   : yanghengxing@idcos.com
# @File    : UserInfo.py
import json
from db import infodb
from db import mmidredis
class User:
    mmid = '' ## 用户id
    dist = '' ##人脉距离
    name = '' ##姓名
    rank = '' ##用户影响力
    position = '' ##公司职位
    company = '' ##公司名称
    schools = '' ##毕业学校
    province = '' ##省份
    city = '' ##城市／区

    def __init__(self,json):

        self.mmid = json['mmid']
        self.dist = json['dist']
        self.name = json['name']
        self.rank = json['rank']
        self.position = json['position']
        self.company = json['company']
        self.province = json['province']
        self.city = json['city']
        try:
            self.schools = json['schools']
            if len(self.schools) > 1:
                self.schools = ','.join(self.schools)
            else:
                self.schools = self.schools[0]
        except:
            self.schools = "no school data"

    def insert(self):
        db = infodb()
        db.insertData(self.mmid,self.dist,self.name,self.rank,self.position,self.company,self.schools,self.city,self.province)



    def getUser(self):
        dict = {'用户编号为':self.mmid,
                '人脉距离为':self.dist,
                '姓名为':self.name,
                '影响力分数为':self.rank,
                '所在省份为':self.province,
                '所在城市为':self.city,
                '教育经历为':self.schools,
                '所在公司为':self.company,
                '所在职位为':self.position}
        return dict