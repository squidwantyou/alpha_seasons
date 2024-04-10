#!/usr/bin/env python
import sys,os
import cards

all_cards = cards.name.values()

all_values = dict()
for key in all_cards:
    all_values[key] = 0

infile = sys.argv[1]

for line in open(infile):
    try:
        items = line.strip().split("\t")
        game_id = items[0] 
        mlist = items[1:10]
        ylist = items[10:19]
        result = items[19]

        all_values[ mlist[0] ] += 8 + 10
        all_values[ mlist[1] ] += 7 + 5
        all_values[ mlist[2] ] += 5
        all_values[ mlist[3] ] += 4
        all_values[ mlist[4] ] += 2
        all_values[ mlist[5] ] += 1
        all_values[ mlist[6] ] += -1
        all_values[ mlist[7] ] += -2
        all_values[ mlist[8] ] += -4

        all_values[ ylist[1] ] += -1
        all_values[ ylist[2] ] += -1
        all_values[ ylist[3] ] += -2
        all_values[ ylist[4] ] += -2
        all_values[ ylist[5] ] += -3
        all_values[ ylist[6] ] += -3
        all_values[ ylist[7] ] += -4
        all_values[ ylist[8] ] += -4
    except:
        pass
    

sorted_keys = sorted( all_cards, key = lambda x:all_values[x], reverse = True )

total = sum( all_values.values() )
count = len( all_cards )
scale = total*1.0/count

for key in sorted_keys:
    print("%5.2f\t%s"%(all_values[key]/scale,key))

