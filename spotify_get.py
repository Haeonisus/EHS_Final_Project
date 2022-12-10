import requests
import json
import csv
import time


def get_artist_info(name, headers):
    
    
    url = "https://api.spotify.com/v1/search"
    param = {
        "q" : name,
        "type" : "artist",
        "limit" : 1
    }
    
    
    
    res = requests.get(url, headers= headers, params = param)
        
    popularity = json.loads(res.text)['artists']['items'][0]['popularity']
    
    name = json.loads(res.text)['artists']['items'][0]['name']
    
    id =   json.loads(res.text)['artists']['items'][0]['id']      
    
    follower = json.loads(res.text)['artists']['items'][0]['followers']['total']
    
    return (id,name, follower, popularity)
        

def get_track_by_artist(headers, id):
    
    url = "https://api.spotify.com/v1/artists/{}/top-tracks".format(id)
    
    params = {
    "market": 'US',
    "limit": "7"
    }
    
    res = requests.get(url, headers = headers, params = params)
    
    data = json.loads(res.text)
    
    return data['tracks']
    
    
    
    
    
def export_csv(info_list, file_name):
    
    with open(file_name, 'w', newline='', encoding= 'utf8') as csvfile:
        
        writer = csv.writer(csvfile)
        writer.writerows(info_list)
    