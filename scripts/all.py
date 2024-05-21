#!/usr/bin/env python
import sys,os

lines = open(sys.argv[1]).readlines()
player_id = lines[0].strip()
player_name = lines[1].strip()
LIMIT = None
try:
    LIMIT = round(float(lines[2].strip())/10)
except:
    LIMIT = 100

os.system(f"python scripts/get_games.py '{player_id}' '{LIMIT}'")
os.system(f"python scripts/grep_table_number.py")
os.system(f"python scripts/download_all.py")

os.system(f"mkdir '{player_name}'")
os.system(f"mv game_log  games table_id.list '{player_name}'")
os.system(f"mv '{player_name}' downloaded_data")

os.chdir(f"downloaded_data/{player_name}")

os.system(f"../../scripts/draft2.py '{player_name}' {player_id} ")
os.system(f"../../scripts/first_hand_rate.py draft_output.csv > first.csv")
os.system(f"../../scripts/tier2.py draft_output.csv > tier.csv")
os.system(f"../../scripts/kept_rate.py draft_output.csv > kept.csv")
os.system(f"../../scripts/played.py '{player_name}' {player_id} ")
os.system(f"../../scripts/played_win_rate.py > played_win_rate.csv")

os.chdir("../..")


