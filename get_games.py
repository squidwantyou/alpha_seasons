#!/usr/bin/env python
import requests

cookies = requests.cookies.RequestsCookieJar()
cookies.set("TournoiEnLigneid","GV87DPsbvz6hP8B")
cookies.set("TournoiEnLignetk","drRzkrUKuXstEa9U8wl0PGySF2ySDmMXf1ru8dl50KsuYvav6nZQjfF4OkAZRvoO")

url = "https://boardgamearena.com/gamestats/gamestats/getGames.html?player=84727173&opponent_id=0&game_id=30&finished=0&page=2&updateStats=0"


headers =  {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6,lb;q=0.5",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-request-token": "GV87DPsbvz6hP8B",
    "x-requested-with": "XMLHttpRequest",
    "referrer": "https://boardgamearena.com/gamestats?player=94020171&opponent_id=85255171&finished=0",
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
    turl = f"https://boardgamearena.com/gamestats/gamestats/getGames.html?player=84727173&opponent_id=0&game_id=30&finished=0&page={i}&updateStats={j}"
    r = requests.get(turl,cookies=cookies, headers = headers )
    with open(f"{i}.json",'w') as ofp:
        ofp.write(r.text)
    print(i,turl)
    if i == 438:
        break
    i += 1





