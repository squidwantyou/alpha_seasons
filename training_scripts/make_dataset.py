#!/usr/bin/env python
import sys,os
import cards
import numpy as np
import pickle
import torch

# load card index
cards_l = list()
for k in sorted(cards.name.keys()):
    cards_l.append( cards.name[k] )

infiles = sys.argv[1:]

all_query = list()
all_label = list()

for infile in infiles:
    for line in open(infile):
        try:
            query = list()
            line = line.strip()
            items = line.split("\t")
            p_hands = [ cards_l.index(x) for x in items[1:10] ]
            y_hands = [ cards_l.index(x) for x in items[10:19]]

            this_list = list()
            that_list = list()
            for i in range(9):
                if i%2==1:
                    this_list.append( p_hands[i] )
                    that_list.append( y_hands[i] )
                else:
                    this_list.append( y_hands[i] )
                    that_list.append( p_hands[i] )

            for i in range(8):
                p1 = [-1,]*9
                p2 = [-1,]*8
                p3 = [-1,]*7
                p4 = [-1,]*6
                choice = [0,]*95
                choice[p_hands[i]] = 1
                #p1
                for _ in range(i, 9):
                    p1[_] = this_list[_]
                #p2
                if i == 0:
                    pass
                else:
                    for _ in range(i+1,9):
                        p2[_-1] = that_list[_]
                #p3
                for _ in range(0,i):
                    p3[_] = p_hands[_]
                #p4
                for _ in range(0,i-1):
                    p4[_] = y_hands[_]

                query = list()
                query.extend( p1 )
                query.extend( p2 )
                query.extend( p3 )
                query.extend( p4 )
                all_query.append( query )
                all_label.append( choice )
        except Exception as e:
            print(e)
            pass

all_query = np.array( all_query )
all_label = np.array( all_label )

all_data = list(zip(all_query,all_label))

with open( 'output.pickle','wb') as ofp:
    pickle.dump( all_data,ofp)


# each data point is 1D Array:   [9][0][0],  [8][1][0],  [7],[2],[1], [6][3][2],  [2],[8],[7] 
# 0  [9], [0]  [0], [0] [1]
# 1  [8], [8], [1], [0] [1]
# 2  [7], [7], [2], [1] [1]
# 3   6    6   3    2   [1]
# 4   5    5   4    3
# 5   4    4   5    4
# 6   3    3   6    5
# 7   2    2   7    6
# max 9    8   7    6 
# from this  that  p  y 
