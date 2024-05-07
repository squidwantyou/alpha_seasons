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
        

with open("draft_output.csv",'w') as ofp:
    for game_id,ming_hand,yeguai_hand,result in all_draft:
        ofp.write(game_id)
        ofp.write("\t")
        ofp.write("\t".join(ming_hand[:9]) )
        ofp.write("\t")
        ofp.write("\t".join(yeguai_hand[:9]) )
        ofp.write("\t")
        ofp.write(str(result))
        ofp.write("\n")

