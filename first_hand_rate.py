#!/usr/bin/env python
import sys,os
import json
import cards
import glob

all_draft = list()
for line in open("draft_output.csv"):
    try:
        line = line.strip()
        items = line.split("\t")
        game_id = items[0]
        ming_hand = items[1:10]
        yeguai_hand = items[10:19]
        result = items[19]
        all_draft.append( (game_id,ming_hand,yeguai_hand,result) )
    except:
        pass

count = dict()
c_win = dict()
c_lose = dict()
for game_id,ming_hand,yeguai_hand,result in all_draft:
    tmp = ming_hand[0] 
    if tmp in count:
        count[tmp] += 1
    else:
        count[tmp] = 1
    if tmp not in c_win:
        c_win[tmp] = 0
        c_lose[tmp] = 0
    if result  == 'Win':
        c_win[tmp] += 1
    else: 
        c_lose[tmp] += 1

sorted_key = sorted( count.keys(), key=lambda x:count[x], reverse=True)
print(f"Total\tWin\tWin_Rate\tCard_Name")
for key in sorted_key:
    if key not in c_win:
        c_win[key] = 0
    print(f"{count[key]}\t{c_win[key]}\t{100.0*c_win[key]/count[key]:6.2f}%\t{key}")

