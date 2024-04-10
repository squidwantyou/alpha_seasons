#!/usr/bin/env python
import requests
import sys,os
import time
import random as rd

lines = open("accounts").readlines()
username = lines[0].strip()
password = lines[1].strip()

# 
player_id = sys.argv[1] 
LIMIT = int(sys.argv[2])
os.system("mkdir games")

# All request in same sesson s
s = requests.Session()

# Open login page and get access token
headers =  {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6,lb;q=0.5",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "Origin": "https://zh-cn.boardgamearena.com",
    "Referer":"https://zh-cn.boardgamearena.com/account",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "",
    "method": "GET",
    "mode": "cors",
    "credentials": "include",
}
r = s.post( "https://zh-cn.boardgamearena.com/account", headers = headers )
tmp = r.content.decode("utf8")
request_token = False
for line in tmp.split("\n"):
    if "requestToken" in line:
        request_token = line.split('\'')[1]
        if request_token:
            break

# login and (automatic) save cookies
data = {
    "email": username,
    "password": password,
    "rememberme": "on",
    "redirect": "join",
    "request_token": request_token,
    "form_id": "loginform",
    "dojo.preventCache": str(int(time.time())),
}

url = "https://zh-cn.boardgamearena.com/account/account/login.html"
r = s.post(url, headers=headers, data=data)
tmp = r.content


# load
neid = s.cookies.get("TournoiEnLigneid")
headers =  {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6,lb;q=0.5",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-request-token": neid,
    "x-requested-with": "XMLHttpRequest",
    "referrer": f"https://boardgamearena.com/gamestats?player={player_id}&finished=0",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "",
    "method": "GET",
    "mode": "cors",
    "credentials": "include",
}

i = 1 
while True:
    if i == 1:
        j = 1
    else :
        j = 0 
    turl = f"https://boardgamearena.com/gamestats/gamestats/getGames.html?player={player_id}&opponent_id=0&game_id=30&finished=0&page={i}&updateStats={j}"
    r = s.get(turl,headers = headers )
    with open(f"games/{i}.json",'w') as ofp:
        ofp.write(r.text)
    print(i,turl)

    if os.path.getsize(f"games/{i}.json") < 400 or i == LIMIT:
        break
    i += 1


