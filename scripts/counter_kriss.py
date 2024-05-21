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

all_counter = dict()
all_help = dict()
for line in open(infile):
    try:
        items = line.strip().split("\t")
        game_id = items[0] 
        mlist = items[1:10]
        ylist = items[10:19]
        result = items[19]
        
        if result.startswith("Lose") and 'Necrotic Kriss' in mlist:
            for card in ylist:
                if card not in all_counter:
                    all_counter[card] = 1
                else:
                    all_counter[card] += 1

        if result.startswith("Win") and 'Necrotic Kriss' in mlist:
            for card in mlist:
                if card not in all_help:
                    all_help[card] = 1
                else:
                    all_help[card] += 1
        
    except Exception as e:
        print(e)

        pass


kept_keys = [ x for x in all_counter if all_counter[x]!=0 ]
sorted_keys = sorted( kept_keys, key = lambda x:all_counter[x], reverse = True )


print("%s\t%s"%("Count","Card"))
for key in sorted_keys:
    print("%5.2f\t%s"%(all_counter[key],key))

kept_keys = [ x for x in all_help if all_help[x]!=0 ]
sorted_keys = sorted( kept_keys, key = lambda x:all_help[x], reverse = True )
print("%s\t%s"%("Count","Card"))
for key in sorted_keys:
    print("%5.2f\t%s"%(all_help[key],key))

