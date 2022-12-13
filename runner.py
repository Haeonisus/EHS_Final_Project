import auth
import spotify_get
import sqlite3
import constructdb
#artist_list = ["BTS", "BLACKPINK", "TWICE", "Stray Kids", "NCT 127", "Big Bang", "KARA", "Girls Generation", "Red Velvet", "Monsta X", "EXO", "GOT 7", "SHINee", "The Boyz", "Pentagon", "Winner", "iKON", "NCT DREAM", "(G)I-DLE"]

def run():
    
    conn = sqlite3.connect("K-POP.db")
    cur = conn.cursor()
    
    user_input = input("First time?: ")
    
    if user_input == 'y':
        constructdb.droptables(conn, cur)
        constructdb.createtables(conn, cur)
    
    headers = auth.auth()
    
    artist = input("Insert your artist: ")

    artist_info = []    
        
    data =spotify_get.get_artist_info(artist, headers)
            
    artist_info.append(data)
        
    artist_id = data[0]
        
    constructdb.insert_artists(conn, cur, artist_info)
    
    track_info = []
        
    tracks = spotify_get.get_track_by_artist(headers, artist_id)
        
    for track in tracks:
        track_info.append((artist_id, track['album']['name'], track['popularity']))

    constructdb.insert_tracks(conn,cur,track_info)
    
    
    
    res = cur.execute("SELECT * FROM artists")
    
    for x in res.fetchall():
        print(x)
    
run()