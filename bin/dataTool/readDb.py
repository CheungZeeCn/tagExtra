#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-05 12:29:41 
# Copyright 2013 NONE rights reserved.

import database
import db_config
import sys


_db = None

def initDb():
    global _db
    try:
        _db = database.Connection(**db_config.gtc_traffic_db)
    except Exception, e:
        print "Exception:", e
        return False
    return True

def query(sql):
    return _db.query(sql)       

def readData(tbl='intro_for_event_extraction', limit=None):
    if limit == None:
        sql = "select * from %s" % (tbl)
    else:
        sql = "select * from %s limit %d" % (tbl, limit)  
    return _db.query(sql)       

def quitDb():
    _db.close()

def getLenOfTbl(tbl):
    sql = 'select count(*) as cnt from %s' % (tbl)
    try:
        ret = _db.query(sql)
        nu = int(ret[0]['cnt'])
    except Exception, e:
        return None 
    return nu 


if __name__ == '__main__':
    if initDb() != True:
        print "exit"
        sys.exit(-1)    
    ret = readData('intro_for_event_extraction', 10)    
    for record in ret:
        print record['introductionSeg']
    quitDb()

