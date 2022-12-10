import matplotlib.pyplot as plt
import sqlite3
import spotify_get

def pop_follow(conn, cur):
    
    res = cur.execute("SELECT followers, popularity FROM artists")
    
    x = []
    y = []
    
    for data in res.fetchall():
        follower, popularity = data
        x.append(follower)
        y.append(popularity)
        
   
    
    plt.scatter(x,y)
    plt.xlabel("number of followers")
    plt.ylabel("popularity")
    plt.title("followers vs popularity")
    plt.show()
    
conn = sqlite3.connect("spotify.db")
cur = conn.cursor()

def consistency(conn, cur):
    
    res = cur.execute("SELECT artist, AVG(track_popularity), popularity FROM artists JOIN tracks USING (artist_id) GROUP BY artist ")
    
    x = []
    y = []
    
    for data in res.fetchall():
        
        artist, avg_pop, pop = data
        
        x.append(artist)
        y.append(avg_pop - pop)
        
    plt.bar(x,y)
    plt.xlabel("artist name")
    plt.ylabel("popularity difference")
    plt.title("artist popularity and track popularity difference")
    plt.show()
    
def popularity(conn, cur):
    
    res = cur.execute("SELECT artist, popularity FROM artists")
    
    x = []
    y = []
    
    for data in res.fetchall():
        
        artist, pop = data
        
        x.append(artist)
        y.append(pop)
        
    plt.bar(x,y)
    plt.xlabel("artist name")
    plt.ylabel("popularity")
    plt.title("artist popularity chart")
    plt.show()
    
def avg_track_pop(conn,cur):
    
    res = cur.execute("SELECT artist, AVG(track_popularity) FROM artists JOIN tracks USING (artist_id) GROUP BY artist ")
    
    info_list = [("Artist","Top 7 Track Average Popularity")]
    
    for data in res:
        artist, pop = data
        
        
        
        info_list.append((artist, "{:.2f}/100".format(pop)))
    
    spotify_get.export_csv(info_list, "popularity_analysis.csv") 
    
        
        
avg_track_pop(conn,cur)
    
popularity(conn, cur)
user_in = input("next?")
pop_follow(conn, cur)
user_in = input("next?")
consistency(conn, cur)
