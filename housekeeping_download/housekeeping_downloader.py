#!/usr/bin/env python
import sys,os

os.chdir("/home/ffallrain/alpha_seasons/housekeeping_download")

os.system("python ./get_games.py")
os.system("python ./grep_table_number.py")

i = 0
username = None
password = None
for line in open("accounts"):
    if i%2 == 0:
        username = line.strip()
    if i%2 == 1:
        password = line.strip()
        os.system(f"python ./get_game_log.py '{username}' '{password}'")
    i += 1
        

