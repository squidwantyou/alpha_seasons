#!/usr/bin/env python
import sys,os
import json
import cards
import glob

all_jsons = glob.glob("game_log/*.json")
all_draft = dict()

if os.path.isfile(sys.argv[1]):
    lines = open(sys.argv[1]).readlines()
    player_name = lines[1].strip()
    player_id = lines[0].strip()
else:
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

        # first player
        start = None
        for log in logs:
            if "/table/t" in log["channel"] :
                for action in log["data"]:
                    if action["type"] == "chooseDie":
                        start_player = action["args"]["player_id"]
                        if start_player == player_id:
                            start = True
                        else:
                            start = False
                        break
                if start != None:
                    break

        # dices set up
        dices = set()
        for log in logs:
            if "/table/t" in log["channel"] :
                for action in log["data"]:
                    if action["type"] == "newDices":
                        for _ in action["args"]["dices"]:
                            dices.add(  str(  (int( _["season"] )-1 )  + (int( _["id"] )-1)*4  ) )
        assert len(dices) == 12
        dices = list( dices )
        dices.sort()

        # result 
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

        # draft cards
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
            
            # done draft, stop analysis, save data
            if done_draft:
                all_draft.append( (game_id,dices,start, ming_hand,yeguai_hand,result) )
                break

    except Exception as e:
        print(e)

with open("start_info.csv",'w') as ofp:
    for game_id,dices,start,ming_hand,yeguai_hand,result in all_draft:
        ofp.write(game_id)
        ofp.write("\t")
        ofp.write("\t".join(dices) )
        ofp.write("\t")
        ofp.write( str(start) )
        ofp.write("\t")
        ofp.write("\t".join(ming_hand[:9]) )
        ofp.write("\t")
        ofp.write("\t".join(yeguai_hand[:9]) )
        ofp.write("\t")
        ofp.write(str(result))
        ofp.write("\n")

