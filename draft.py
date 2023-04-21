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
        

        logs = a['data']['data']['data']

        macao_list = list()
        yeguai_list = list()
        macao_hand = list()
        yeguai_hand = list()

        for log in logs[:4]:
            packet_id = int(log['packet_id'])
            channel = log['channel']
            if 'player' in channel :
                if log['data'][0]['type'] == 'newCardChoice':
                    t = log['data'][0]['type']
                    args = log['data'][0]['args']
                    if channel == '/player/p84727173' :
                        for card in args['cards']:
                            tmp = cards.name[card['type']]
                            macao_hand.append(tmp)
                    else:
                        for card in args['cards']:
                            tmp = cards.name[card['type']]
                            yeguai_hand.append(tmp)
            
        for log in logs:
            packet_id = int(log['packet_id'])
            channel = log['channel']
            if 'player' in channel :
                t = log['data'][0]['type']
                args = log['data'][0]['args']
                if channel == '/player/p84727173' :
                    if t == 'pickPowerCard':
                        tmp = cards.name[args['card']['type']]
                        if len(macao_list) < 8:
                            macao_list.append(tmp)
                else:
                    if t == 'pickPowerCard':
                        tmp = cards.name[args['card']['type']]
                        if len(yeguai_list) < 8:
                            yeguai_list.append(tmp)

            if log['data'][0]['type'] == 'placeMyInLibrarynew':
                
                for tmplog in logs:
                    if tmplog['data'][0]['type'] == 'playerConcedeGame':
                        if tmplog['data'][0]['args']['player_id'] != '84727173':
                            result[game_id] = "Win"
                        else:
                            result[game_id] = "Lose"
                        break

                for tmplog in logs:
                    if 'player' not in tmplog['channel']:
                        for block in tmplog['data']:
                            if block['type'] == 'simpleNode':
                                if "End of game" in block['log']:
                                    if "End of game (tie)" in block['log']:
                                        result[game_id] = "Draw"
                                    else:
                                        winner = block['args']['player_name']
                                        if winner == 'umegf':
                                            result[game_id] = "Win"
                                        else:
                                            result[game_id] = "Lose"
                                    break

        all_draft[game_id] = ( macao_hand, yeguai_hand, macao_list,yeguai_list ) 
    except Exception as e:
        print(infile)
        print(e)

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


