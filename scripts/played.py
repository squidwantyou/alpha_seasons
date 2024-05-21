#!/usr/bin/env python
import sys,os
import json
import cards
import glob

all_jsons = glob.glob("game_log/*.json")

if os.path.isfile(sys.argv[1]):
    lines = open(sys.argv[1]).readlines()
    player_name = lines[1].strip()
    player_id = lines[0].strip()
else:
    player_name = sys.argv[1] # "chenymandy"
    player_id = sys.argv[2] # "92017275"

all_played = list()
for infile in all_jsons:
    try :
        game_id = infile.split('/')[1].strip(".json")
        a = json.load(open(infile))

        logs = a['data']['logs']

        if len( a['data']['players'] ) != 2:
            continue

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

        if not result:
            result = "Draw"

        played_cards = list()
        for log in logs:
            for action in log["data"]:
                if action["type"] == "summon":
                    if action['args']['player_id'] == player_id:
                        played_cards.append(cards.name[action['args']['card']['type']])

        all_played.append((game_id,result,played_cards))

    except Exception as e:
        print(e)
        
with open("played_cards.csv",'w') as ofp:
    for game_id,result,played_cards in all_played:
        ofp.write(game_id)
        ofp.write("\t")
        ofp.write(result)
        ofp.write("\t")
        ofp.write("\t".join(played_cards))
        ofp.write("\n")

