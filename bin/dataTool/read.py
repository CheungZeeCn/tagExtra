#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# by zhangzhi @2013-11-04 20:03:28 
# Copyright 2013 NONE rights reserved.
import csv
import sys

fName = 'Train.csv'

if __name__ == '__main__':
    lines = 10
    if len(sys.argv) >= 2:
        lines = int(sys.argv[1])
    r = csv.reader(open(fName), delimiter=",", doublequote=True)           
    for each in r:
        print each
        #raw_input()
