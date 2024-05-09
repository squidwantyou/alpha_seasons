#!/usr/bin/env python
import sys,os
import json
import cards
import glob

all_played = list()
for line in open("played_cards.csv"):
    items = line.strip().split("\t")
    try:
        game_id = items[0]
        result = items[1]
        played_cards = items[2:]
        all_played.append( (result,played_cards) )
    except:
        pass

count = dict()
c_win = dict()
c_lose = dict()

for result,played_cards in all_played:
    for card in tuple(played_cards):
        if card not in count:
            count[card] = 0
            c_win[card] = 0
            c_lose[card] = 0
        count[card] += 1
        if result  == 'Win':
            c_win[card] += 1
        else: 
            c_lose[card] += 1

sorted_key = sorted( count.keys(), key=lambda x:100.0*c_win[x]/count[x], reverse=True)
print(f"Total\tWin\tWin_Rate\tCard_Name")
for key in sorted_key:
    if key not in c_win:
        c_win[key] = 0
    print(f"{count[key]}\t{c_win[key]}\t{100.0*c_win[key]/count[key]:6.2f}%\t{key}")

