#!/usr/bin/env python
import sys,os
import json
import glob

dirs = glob.glob("input/*.input")

os.system(f"mkdir table_ids")

for d in dirs:
    player_name = d.split("/")[1].strip(".input")
    with open(f"table_ids/{player_name}_table_id.list",'w') as ofp:
        i = 1
        while True:

            a = json.load(open(f'games/{player_name}/{i}.json'))

            for table in a['data']['tables']:
                if table['normalend'] == '1':
                    if len( table['ranks'].split(',') ) == 2:
                        ofp.write(f"{table['table_id']}\n" )

            i += 1    
            if not os.path.isfile(f"games/{player_name}/{i}.json"):
                break

