#!/usr/bin/env python
import sys,os
import glob 
import matplotlib.pyplot as plt
import numpy as np

files = glob.glob("*/kept.csv")
files.sort()

players = [ x.split("/")[0] for x in files ]


all_seq = dict()
for p,f in zip(players,files):
    lines = open(f).readlines()[1:]
    seq = [ x.strip().split("\t")[1] for x in lines ]
    all_seq[p] = seq


def corr(a,b):
    assert len(a) == len(b)
    N = len(a)
    corr_seq = list()
    for i in range(N):
        seta = set( a[:i+1] )
        setb = set( b[:i+1] )
        common = len(seta & setb)
        corr_seq.append( 1.0 * common / (i+1) )
    return sum(corr_seq)/N
    
print("\n")
print("%20s"%'',end = '')
for i in range(len(players)):
    print("%12s"%players[i][:11],end='')
print('\n')
    

for i in range(len(players)):
    print("%20s"%players[i],end = '')
    for j in range(len(players)):
        print("%12.3f"%(corr(all_seq[players[i]],all_seq[players[j]]) ), end='' )
    print("\n")

    
    
