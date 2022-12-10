import sqlite3


def createtables(conn, cur):
    
    cur.execute("CREATE TABLE IF NOT EXISTS artists(artist_id TEXT PRIMARY KEY, artist TEXT, followers INT, popularity INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS tracks(artist_id TEXT, track_name TEXT PRIMARY KEY, track_popularity INT)")

    conn.commit()
    
def droptables(conn, cur):
    cur.execute("DROP TABLE IF  EXISTS artists")
    cur.execute("DROP TABLE IF  EXISTS tracks")

    conn.commit()
    
    
def insert_artists(conn, cur, info):
    
    cur.executemany("INSERT OR IGNORE INTO  artists VALUES(?,?,?,?)", info)
    
    conn.commit()
     
def insert_tracks(conn, cur, info):
    
    cur.executemany("INSERT OR IGNORE INTO  tracks VALUES(?,?,?)", info)
    
    conn.commit()