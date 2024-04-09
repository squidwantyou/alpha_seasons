#!/usr/bin/env python
import sys,os
import json
import cards
import glob

all_jsons = glob.glob("game_log/*.json")
all_draft = dict()
result = dict()

for infile in all_jsons:
    try :
        game_id = infile.split('/')[1].strip(".json")
        a = json.load(open(infile))

        logs = a['data']['logs']

        if len( a['data']['players'] ) != 2:
            continue

        ming_list = list()
        yeguai_list = list()
        ming_hand = list()
        yeguai_hand = list()

        done_draft = False
        for log in logs:
            if log["channel"] == "/player/p92017275":
                for action in log["data"]:
                    if action["type"] == "pickPowerCard":
                        card = log["data"][0]["args"]["card"]["type"]
                        ming_hand.append(cards.name[card])
                    elif action["type"] == "discard":
                        ming_hand.pop()
            elif "/player/p" in log["channel"] :
                for action in log["data"]:
                    if action["type"] == "pickPowerCard":
                        card = log["data"][0]["args"]["card"]["type"]
                        yeguai_hand.append(cards.name[card])
                    elif action["type"] == "discard":
                        yeguai_hand.pop()
            else:
                pass

            for action in log["data"]:
                if action["type"] == "placeMyInLibrarynew":
                    done_draft = True

            if done_draft:
                break

        result = False
        for log in logs:
            if "/table/t" in log["channel"] :
                for action in log["data"]:
                    if action["type"] == "simpleNode":
                        if "wins!" in action["log"]:
                            if action["args"]["player_name"] == "chenymandy":
                                result = "Win"
                            else:
                                result = "lose"
            if result:
                break

        print(game_id)
        print(" ".join(ming_hand), )
        print(" ".join(yeguai_hand) )
        print( result )



    except Exception as e:
#        print(infile)
        print(e)


if False:
    for key in all_draft:
    #   if result[key] == 'Draw':
           print(key,end=',')
           macao_hand, yeguai_hand, macao_list,yeguai_list = all_draft[key]
           print(",".join(macao_hand),end=',')
           print(",".join(yeguai_hand),end=',')
           print(",".join(macao_list),end=',')
           print(",".join(yeguai_list),end=',')
           print( result[key],end='\n')

sys.exit()

        
count = dict()
c_win = dict()
c_lose = dict()
for key in all_draft:
    tmp = all_draft[key][0][0] 
    if tmp in count:
        count[tmp] += 1
    else:
        count[tmp] = 1
    if key not in result:
        print(key)
    if key in result and result[key] == 'Win':
        if tmp in c_win:
            c_win[tmp] += 1
        else:
            c_win[tmp] = 1


sorted_key = sorted( count.keys(), key=lambda x:count[x], reverse=True)
for key in sorted_key:
    if key not in c_win:
        c_win[key] = 0
    print(f"{count[key]}\t{c_win[key]}\t{100.0*c_win[key]/count[key]:6.2f}%\t{key}")


