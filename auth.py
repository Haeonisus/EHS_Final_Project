import requests
import base64
import json
import csv
from secrets import *

def auth():
    
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}
    file = open("pass.txt", 'r', encoding = 'utf8')
    p = file.read()
    cid, csec = p.split(",")[0], p.split(",")[1]
    info = "{}:{}".format(cid, csec)
    infoBytes = info.encode('ascii')
    bytes = base64.b64encode(infoBytes)
    message = bytes.decode('ascii')
    
    headers['Authorization'] = "Basic {}".format(message)
    data['grant_type'] = "client_credentials"
    
    res = requests.post(url, headers=headers, data=data)

    access_token = res.json()['access_token']
    
    headers = {
    "Authorization": "Bearer " + access_token
    }

    return headers