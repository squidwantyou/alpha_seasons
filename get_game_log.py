#!/usr/bin/env python
import requests
import time
import sys,os
import random

start = int(sys.argv[1])
LIMIT = 200

s = requests.Session()

neid = sys.argv[2] # "Opwm2hxYefWNRqL"
netk = sys.argv[3] # "K2B2yQsk0tLaGep1Qz1Y8Scdh1pX84anFNi1vIspVt7oN9gubcz6hgj25mXJprG4"

#cookies = requests.cookies.RequestsCookieJar()
#cookies.set("TournoiEnLigneid","GV87DPsbvz6hP8B")
#cookies.set("TournoiEnLignetk","drRzkrUKuXstEa9U8wl0PGySF2ySDmMXf1ru8dl50KsuYvav6nZQjfF4OkAZRvoO")
s.cookies.set("TournoiEnLigneid",neid,domain=".boardgamearena.com")
s.cookies.set("TournoiEnLignetk",netk,domain=".boardgamearena.com")

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
    # "x-request-token": "x1bXyQxUJAGm8AC",
    "x-requested-with": "XMLHttpRequest",
    "referrer": "https://boardgamearena.com",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "",
    "method": "GET",
    "mode": "cors",
    "credentials": "include",
}

url =  f"https://boardgamearena.com/gamereview?table=366498894"
r = s.get(url, headers = headers )

os.system("mkdir game_log")

i = 0 
count = 0 
for line in open("table_id.list") :
    i += 1
    if i<= start:
        continue
    if count == LIMIT:
        break
    count += 1

    inid = line.strip()
    # inid = "366477213"

    url = f"https://boardgamearena.com/gamereview/gamereview/requestTableArchive.html?table={inid}&dojo.preventCache={int(time.time())}"
    r = s.get(url, headers = headers )
#    print(r.headers)
    b = r.text
    time.sleep( random.random() )

    url = f"https://boardgamearena.com/archive/archive/logs.html?table={inid}&translated=true&dojo.preventCache={int(time.time())}"
    headers['referrer'] = f"https://boardgamearena.com/gamereview?table={inid}"
    r = s.get(url, headers = headers )

    with open(f"game_log/{inid}.json",'w') as ofp:
        ofp.write(r.text)

    print(i,inid)
    print(url)
    time.sleep( random.random() )

    


