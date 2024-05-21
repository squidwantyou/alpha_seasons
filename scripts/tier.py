#!/usr/bin/env python
import sys,os
import cards

all_cards = cards.name.values()

all_values = dict()
for key in all_cards:
    all_values[key] = 0

infile = sys.argv[1]


for line in open(infile):
    items = line.split(",")
    mlist = items[19:27]
    ylist = items[27:35]

    mhand = items[1:10]
    yhand = items[10:19]

    for i in range(8):
        choice = mlist[i]
        failed = list()
        if i%2 == 0:
            a = mhand[:]
            for j in range(i):
                if j%2==0:
                    a.remove( mlist[j] )
                else:
                    a.remove( ylist[j] )
        else:
            a = yhand[:]
            for j in range(i):
                if j%2==0:
                    a.remove( ylist[j] )
                else:
                    a.remove( mlist[j] )
        
        a.remove(choice)
        all_values[choice] += len(a)
        if len(a) == 8:
            all_values[choice] += 10
        if len(a) == 7:
            all_values[choice] += 5

        for tmp in a:
            all_values[tmp] += -1

sorted_keys = sorted( all_cards, key = lambda x:all_values[x], reverse = True )

for key in sorted_keys:
    print(all_values[key],"\t",key)

