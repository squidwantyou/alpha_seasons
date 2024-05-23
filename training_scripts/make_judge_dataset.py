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
            line = line.strip()
            items = line.split("\t")
            dices   = [           int(x) for x in items[1:13]  ]
            p_hands = [ cards_l.index(x) for x in items[13:22] ]
            y_hands = [ cards_l.index(x) for x in items[22:31] ]
            result = 1 if items[-1] == 'Win' else -1

            dice_query = [0,]*20
            for _ in dices:
                dice_query[_] += 1

            query = [0,]*(95*2) + dice_query
            for _ in p_hands:
                query[_] += 1
            for _ in y_hands:
                query[_+95] -= 1
            all_query.append(query)
            all_label.append([result,])

            query = [0,]*(95*2) + dice_query
            for _ in p_hands:
                query[_+95] -= 1
            for _ in y_hands:
                query[_] += 1

            all_query.append(query)
            all_label.append([0-result,])

            print(query,result)

        except Exception as e:
            print(e)
            pass

all_query = np.array( all_query )
all_label = np.array( all_label )

all_data = list(zip(all_query,all_label))

with open( 'output_judge.pickle','wb') as ofp:
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
