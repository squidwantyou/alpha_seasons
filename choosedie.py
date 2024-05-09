#!/usr/bin/env python
import sys,os
import json
import glob
import pickle

all_jsons = glob.glob("game_log/*.json")

if os.path.isfile(sys.argv[1]):
    lines = open(sys.argv[1]).readlines()
    player_name = lines[1].strip()
    player_id = lines[0].strip()
else:
    player_name = sys.argv[1] # "chenymandy"
    player_id = sys.argv[2] # "92017275"

die_faced = {
}
all_choice = list()
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

        choice_seq = list()
        time = [1,1]
        for log in logs:
            for action in log["data"]:
                if action["type"] == "chooseDie":
                    cate = None
                    if action['args']['player_id'] == player_id:
                        cate = 'p'
                    else:
                        cate = 'o'
                    die_type = action['args']['die_type']
                    choice_seq.append( (time,cate,die_type) )
                elif action['type'] == 'timeProgression':
                    month = action['args']['month']
                    year  = action['args']['year']
                    time = [year,month]
                elif action['type'] == 'newDices':
                    dices = list()
                    for _ in action['args']['dices']:
                        dices.append( _['season']+_["id"]+_["face"] )
                    choice_seq.append( [time,'all',dices] )

        all_choice.append((game_id, result,choice_seq))

    except Exception as e:
        print(e)
        

pickle.dump( all_choice, open("dice_data.pickle",'wb') )

