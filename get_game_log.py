#!/usr/bin/env python
import requests
import time
import sys,os
import random


LIMIT = 200
s = requests.Session()
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
    "referrer": "https://boardgamearena.com",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "",
    "method": "GET",
    "mode": "cors",
    "credentials": "include",
}

os.system("mkdir game_log")

i = 0 
count = 0 
for line in open("table_id.list") :
    inid = line.strip()

    if os.path.isfile(f"game_log/{inid}.json"):
        continue
    else:
        pass

    i += 1
    if count == LIMIT:
        break
    count += 1

    url = f"https://boardgamearena.com/gamereview/gamereview/requestTableArchive.html?table={inid}&dojo.preventCache={int(time.time())}"
    r = s.get(url, headers = headers )
    b = r.text
    time.sleep( random.random() )

    url = f"https://boardgamearena.com/archive/archive/logs.html?table={inid}&translated=true&dojo.preventCache={int(time.time())}"
    headers['referrer'] = f"https://boardgamearena.com/gamereview?table={inid}"
    r = s.get(url, headers = headers )

    with open(f"game_log/{inid}.json",'w') as ofp:
        ofp.write(r.text)

    statue = True
    if os.path.getsize(f"game_log/{inid}.json") < 200:
        os.system(f"rm game_log/{inid}.json")
        statue = False

    print(i,inid,statue)
    time.sleep( random.random() )

