#!/usr/bin/env python
import sys,os
for line in open(sys.argv[1]):
    n = len(line.split("\t")) - 2
    if n >= 30:
        print(line.split("\t")[0],n)
