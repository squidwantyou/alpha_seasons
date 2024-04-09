#!/usr/bin/env python
import requests

neid = "EY1dk77B6i2e3Lm"
netk = "CtUa7sNKuEmAFpUKn5Y87p90uTVQtP8KTGwLFVT17jxwa6rlZUXBjO7BJxZkcQK3"

cookies = requests.cookies.RequestsCookieJar()
cookies.set("TournoiEnLigneid",neid)
cookies.set("TournoiEnLignetk",netk)

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
    "referrer": "https://boardgamearena.com/gamestats?player=92017275&finished=0",
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
    turl = f"https://boardgamearena.com/gamestats/gamestats/getGames.html?player=92017275&opponent_id=0&game_id=30&finished=0&page={i}&updateStats={j}"
    r = requests.get(turl,cookies=cookies, headers = headers )
    with open(f"{i}.json",'w') as ofp:
        ofp.write(r.text)
    print(i,turl)
    if i == 500:
        break
    i += 1


