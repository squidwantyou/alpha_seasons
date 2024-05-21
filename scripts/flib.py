#!/usr/bin/env python
import requests
import time
import sys,os
import random
import json


def get_id(query):
    lines = open("accounts").readlines()
    username = lines[0].strip()
    password = lines[1].strip()

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

    # Get game log per table id 
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

    # get log request 
    url = f"https://boardgamearena.com/omnibar/omnibar/search.html?query={query}"
    headers['referrer'] = f"https://boardgamearena.com/"
    r = s.get(url, headers = headers )
    a = json.loads(r.text )
    i = (a["data"]["players"][0]['id'])
    return i


