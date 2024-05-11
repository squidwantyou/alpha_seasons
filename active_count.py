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


ctime = 0
n = 0
count = dict()
for infile in all_jsons:
    n += 1
    try :
        game_id = infile.split('/')[1].strip(".json")
        a = json.load(open(infile))

        logs = a['data']['logs']

        if len( a['data']['players'] ) != 2:
            continue

        for log in logs:
            for action in log["data"]:
                if action["type"] == "active":
                    if action["args"]["player_id"] == player_id:
                        name = action["args"]["card_name"]
                        if name in count:
                            count[name][0] += 1
                            count[name].append( game_id )
                        else:
                            count[name] = [1,game_id]

    except Exception as e:
        pass
        
with open("active.csv",'w') as ofp:
    for a in sorted(count.keys(), key=lambda x:count[x], reverse = True):
        ofp.write( "%30s\t%8d\t%8.3f\n"%(a,count[a][0],count[a][0]*1.0/n) )
