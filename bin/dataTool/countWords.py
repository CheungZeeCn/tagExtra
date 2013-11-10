#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-09-28 16:59:38 
# Copyright 2013 NONE rights reserved.

import sys
import re
import database
import db_config
import readDb
import time
from collections import Counter

reEmpty = re.compile(r'\s+')
#rePunc = re.compile(r'^\W+|(-"|\W+)$')
#rePunc = re.compile(r'^\W+')
g_stopWordSet = set()

def getWordsFromLine(aLine):
    """get word list from a line"""
    retList = []
    if aLine == '':
        return []
    for word in reEmpty.split(aLine.strip().lower()):
        """!"#$%&\'()*+,.-_/:;<=>?@[\\]^`{}|~"""
        word = word.lstrip('!"#$%&\'()*+,-_/:;<=>?@[\\]^`{}|~').rstrip('!"$%&\'()*,-_./:;<=>?@[\\]^`{}|~')
        if word not in ('', 'p', 'pre', 'h') and not isStopWord(word):
            retList.append(word)
    return retList

def isStopWord(word):
    if word in g_stopWordSet:
        return True
    else:
        return False

def initStopWordList():
    "set up"
    global g_stopWordSet
    #force it to read
    sys.argv.append('./stopwords1.txt')
    sys.argv.append('./stopwords2.txt')
    if len(sys.argv) > 1:
        for each in sys.argv[1:]:
            with open(each) as f:         
                g_stopWordSet |= set([ word.strip() for word in f ])
    return True     

def readTrainData(begin=0, lenth=10000):
    tbl = 'tag_train_l'
    sql = "select * from %s limit %d, %d" % (tbl, begin, lenth)
    print sql 
    ret = readDb.query(sql)
    print ret
    return ret

def countWord(data):
    wDict = {}
    lines = data.split("\n")
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        for w in getWordsFromLine(line):
            if w not in wDict:
                wDict[w] = 0 
            wDict[w] += 1
    return wDict

if __name__ == '__main__':
    print "#init db"
    if readDb.initDb() != True:
        sys.exit(-1)
    print "#stopwords db"
    initStopWordList()
    
    print "counting #records:"
    nuOfData = readDb.getLenOfTbl('tag_train_l')
    print nuOfData
    nuOfData = 1


    g_wordCount = {}
    g_tagCount = {}

    g_wordList = []
    g_wordCode = {}
    g_tagList = []
    g_tagCode = {}

    last = 10000; lenth = 100
    while True:
        status = last*1.0/nuOfData * 100
        data = readTrainData(last, lenth)
        lenOfData = len(data)
        #dealing
        for rec in data:
            recId = rec['id']
            recBody = rec['body']
            recTitle = rec['title']
            recTag = rec['tag']
            wCount = countWord(recTitle + ' '+recBody)
            tCount = dict(Counter(countWord(recTag)))
            wDict = {}
            tDict = {}
            for w in wCount:
                if w not in g_wordCode:
                    g_wordCode[w] = len(g_wordList)
                    g_wordList.append(w)
                wCode = g_wordCode[w]
                wDict[wCode] = wCount[w]
            for t in tCount:
                if t not in g_tagCode:
                    g_tagCode[t] = len(g_tagList)
                    g_tagList.append(t)
                tCode = g_tagCode[t]
                tDict[tCode] = tCount[t]

            g_wordCount[recId] = wDict      
            g_tagCount[recId] = tDict      
            
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S', \
                    time.localtime(time.time()))
        print "%.2f%%||%s" % (status, timeStr)
        last += lenOfData
        if lenOfData == 0 or True:
            break
        

    print g_wordCode
    print g_wordList
    print g_wordCount
    print g_tagCode
    print g_tagList
    print g_tagCount

