#!/usr/bin/env python
import sys,os
import json
import cards
import glob

all_jsons = glob.glob("game_log/*.json")
all_draft = dict()

player_name = sys.argv[1] # "chenymandy"
player_id = sys.argv[2] # "92017275"

all_draft = list()
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


        result = False
        for log in logs:
            if "/table/t" in log["channel"] :
                for action in log["data"]:
                    if action["type"] == "simpleNode":
                        if "wins!" in action["log"]:
                            if action["args"]["player_name"] == player_name:
                                result = "Win"
                            else:
                                result = "Lose"
            if result:
                break

        done_draft = False
        for log in logs:
            if log["channel"] == f"/player/p{player_id}":
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
                all_draft.append( (game_id,ming_hand,yeguai_hand,result) )
                # print(game_id)
                # print(" ".join(ming_hand), )
                # print(" ".join(yeguai_hand) )
                # print( result )
                break

    except Exception as e:
        print(e)
        
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


