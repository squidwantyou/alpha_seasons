#!/usr/bin/env python
import sys,os
import json

with open("table_id.list",'w') as ofp:
    i = 1
    while True:

        a = json.load(open(f'games/{i}.json'))

        for table in a['data']['tables']:
            if table['normalend'] == '1':
                if len( table['ranks'].split(',') ) == 2:
                    ofp.write(f"{table['table_id']}\n" )

        i += 1    
        if not os.path.isfile(f"games/{i}.json"):
            break

