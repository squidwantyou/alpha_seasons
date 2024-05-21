#!/usr/bin/env python
import sys,os

s = 0
i = 0
for line in open(sys.argv[1]):
    n = len(line.split("\t")) - 2
    s += n
    i += 1
    #if n >= 30:
    #    print(line.split("\t")[0],n)

print("%20s %8d %8d %10.3f"%(sys.argv[2],s,i,s*1.0/i))

