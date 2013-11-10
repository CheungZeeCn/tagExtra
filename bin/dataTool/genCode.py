#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-09-28 16:59:38 
# Copyright 2013 NONE rights reserved.

import sys
import re
import time
import pickle
from collections import Counter
import csv

reEmpty = re.compile(r'\s+')
#rePunc = re.compile(r'^\W+|(-"|\W+)$')
#rePunc = re.compile(r'^\W+')
g_stopWordSet = set()

g_wordCount = {}
g_tagCount = {}
g_wordList = []
g_wordCode = {}
g_tagList = []
g_tagCode = {}

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

def dump2Pickle(data, fname):
    print "dump into [%s]" % (fname)
    #print data
    with open(fname, 'w') as f:
        pickle.dump(data, f)
    print "done"

def showStatus(last, nuOfData):
    global g_wordList
    global g_tagList 
    status = (last*1.0/nuOfData) * 100
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S', \
                time.localtime(time.time()))
    print "%d|%d|%.2f%%|worList:%d|tagList:%d|%s" % (last, nuOfData, status, \
                                        len(g_wordList), len(g_tagList), timeStr)

if __name__ == '__main__':
    nuOfData = 6034195

    last = 0; step = 50000
    cnt = 0
    showStatus(last, nuOfData)

    with open('Train_noHead.csv', 'rb') as f:
        reader = csv.reader(f)
        for rec in reader:
            cnt += 1
            last += 1
            recId = int(rec[0])
            recBody = rec[2]
            recTitle = rec[1]
            recTag = rec[3]
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

            #g_wordCount[recId] = wDict      
            #g_tagCount[recId] = tDict      

            if cnt == step:
                cnt = 0
                showStatus(last, nuOfData)

    showStatus(last, nuOfData)

    print "Done, howManyWords:[%d]. howManyTags[%d] " \
        % (len(g_wordList), len(g_tagList))

    print "we begin to Dump file"       
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S', \
                time.localtime(time.time()))
    print "%s" % (timeStr)
    # dump g_wordCount, g_wordList, g_wordCode
    dump2Pickle(g_wordCount, 'g_wordCount.pickle')
    dump2Pickle(g_wordList, 'g_wordList.pickle')
    dump2Pickle(g_wordCode, 'g_wordCode.pickle')
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S', \
                time.localtime(time.time()))
    print "%s" % (timeStr)
    # dump g_tagCount, g_tagList, g_tagCode
    dump2Pickle(g_tagCount, 'g_tagCount.pickle')
    dump2Pickle(g_tagList, 'g_tagList.pickle')
    dump2Pickle(g_tagCode, 'g_tagCode.pickle')
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S', \
                time.localtime(time.time()))
    print "%s" % (timeStr)
    print "Done, exit"       

