#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-07 14:58:58 
# Copyright 2013 NONE rights reserved.

import re

if __name__ == '__main__':
    tag_all = open("tag_all", "r")
    tag_line = open("tag_line", "w")
    reHavePunc = re.compile("\W+")

    wordSet = set()
    puncSet = set()

    for line in tag_all:
        words = line.strip().split(" ")
        for word in words: 
            tag_line.write("%s\n" % (word))
            ret = reHavePunc.findall(word)
            if ret:
                wordSet.add(word)
                for punc in ret:
                    puncSet.add(punc) 
    wordSetF = open("word_set", "w")
    puncSetF = open("punc_set", "w")
    for each in wordSet:
        wordSetF.write("%s\n" % each)
    for each in puncSet:
        puncSetF.write("%s\n" % each)

    wordSetF.close()
    puncSetF.close()
    tag_all.close()
    tag_line.close()
    print "OK"



    

