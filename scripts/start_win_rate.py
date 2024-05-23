#!/usr/bin/env python
import sys,os
import json
import cards
import glob

s_w = 0
s_l = 0
e_w = 0
e_l = 0
try:
    name = sys.argv[1]
except :
    name = "Name"

for line in open("start_info.csv"):
    items = line.strip().split("\t")
    try:
        game_id = items[0]
        # dices = items[1:13]
        start = items[13]
        result = items[-1]
        if start == "True" and result == "Win":
            s_w += 1
        elif start == "True" and result == "Lose":
            s_l += 1
        elif start == "False" and result == "Win":
            e_w += 1
        elif start == "False" and result == "Lose":
            e_l += 1
    except:
        pass

o_wr = ( s_w + e_w ) / ( s_w + s_l + e_w + e_l )
s_wr =  s_w / (s_w+s_l)
e_wr =  e_w / (e_w+e_l)
yun =  ( s_w + s_l ) / ( s_w + s_l + e_w + e_l )

print(f"{name:25s}\tOverall_win_rate: {o_wr:8.3f}\tStart_win_rate: {s_wr:8.3f}\tNonstart_win_rate: {e_wr:8.3f}\tLuck: {yun:8.3f}")


