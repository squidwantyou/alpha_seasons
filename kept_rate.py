#!/usr/bin/env python
import sys,os
import cards

all_cards = cards.name.values()

all_count = dict()
kept_count = dict()
for key in all_cards:
    all_count[key] = 0
    kept_count[key] = 0

infile = sys.argv[1]

for line in open(infile):
    try:
        items = line.strip().split("\t")
        game_id = items[0] 
        mlist = items[1:10]
        ylist = items[10:19]
        result = items[19]
        
        all_seen = mlist + ylist[1:]
        
        candi = set(all_seen)
        
        for card in candi:
            all_count[card] += all_seen.count(card)
            kept_count[card] += mlist.count(card)
    except:
        pass


kept_keys = [ x for x in all_count if all_count[x]!=0 ]

sorted_keys = sorted( kept_keys, key = lambda x:kept_count[x]*1.0/all_count[x], reverse = True )


print("%s\t%s"%("Keep_Rate","Card"))
for key in sorted_keys:
    print("%5.2f\t%s"%(kept_count[key]*1.0/all_count[key],key))

