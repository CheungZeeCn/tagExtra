#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-18 19:57:05 
# Copyright 2013 NONE rights reserved.

import csv
import util
fName = 'm.20131118205212.pickle'
testName = 'Test_nohead.csv'
k = 5

def loadM(fName):
    return util.loadPickle(fName)

def simi(tagWc, wc):
    v = 0
    tagKeys = set(tagWc.keys())
    keys = set(wc.keys())
    common = tagKeys & keys 
    for w in common:
        v += wc[w]
    return v 

def predict(m, wcDict, k):
    tagV = {}
    for tag in m:
        v = simi(m[tag], wcDict)
        tagV[tag] = v
    values = sorted(tagV.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    topk = values[:k] 
    return [ each[0] for each in topk]

def runTest(testName):
    m = loadM(fName)
    output = []
    c = 0
    with open(testName, 'r') as f:
        reader = csv.reader(f) 
        for line in reader:
            c += 1
            recId = line[0] 
            q = util.yluClean(line[1])
            d = util.yluClean(line[2])
            wcDict = util.countWordLazy(q+d)
            tags = predict(m, wcDict, k)
            output.append([recId, tags])
            #if c == 10:
            #    break
    return output

if __name__ == '__main__':
    timeStmp =  util.getTimeStamp()
    fout = 'tag_out%s.txt' % timeStmp
    out = runTest(testName)
    with open(fout, 'w') as f:
        for each in out:
            recId = each[0]
            tags = " ".join(each[1])
            line = "%s\t%s\n" % (recId, tags)
            print line,
            f.write(line)
    
