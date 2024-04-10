#!/usr/bin/env python
import sys,os

i = 0
username = None
password = None
for line in open("accounts"):
    if i%2 == 0:
        username = line.strip()
    if i%2 == 1:
        password = line.strip()
        os.system(f"python get_game_log.py '{username}' '{password}'")
    i += 1
        
