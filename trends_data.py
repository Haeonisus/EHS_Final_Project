from serpapi import GoogleSearch
import json
import sqlite3
import requests

def set_connector():
    '''Set the connector and cursor'''

    conn = sqlite3.connect('K-POP.db')
    cur = conn.cursor()
    return conn, cur

def get_data() :
    params = {
        "api_key": "ada9cfe28fcdf8fb00125c01d68c6471449a3e8a2be8228a15ba33d5d40795a4",
        "device": "desktop",
        "engine": "google_trends",
        "q": "BTS, BLACKPINK, TWICE, Stray Kids, NCT 127",
        "cat": "3",
        "date": "2003-01-01 2021-12-31",
        "data_type": "TIMESERIES"
    }

    search = GoogleSearch(params)
    results = search.get_json()
    return results

def set_table(cur, conn, data):
    '''Set the table'''

    cur.execute('''DROP TABLE IF EXISTS trends''')
    cur.execute('''CREATE TABLE IF NOT EXISTS trends(id INTEGER PRIMARY KEY, date TEXT, BTS INTEGER, BLACKPINK INTEGER, TWICE INTEGER, StrayKids INTEGER, NCT127 INTEGER)''')
    conn.commit()

    date = []
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    group5 = []
    for i in data['interest_over_time']['timeline_data']:
        date.append((i['date']))
        group1.append((i['values'][0]['extracted_value']))
        group2.append((i['values'][1]['extracted_value']))
        group3.append((i['values'][2]['extracted_value']))
        group4.append((i['values'][3]['extracted_value']))
        group5.append((i['values'][4]['extracted_value']))
    
    years = {}

    for i in range(2003, 2022):
        years[i] = {'BTS':0, 'BLACKPINK':0, 'TWICE':0, 'Stray Kids':0, 'NCT 127':0}
    
    for i in range(len(group1)):
        fulldate = date[i]
        year = int(fulldate[-4:])
        years[year]['BTS'] += group1[i]
        years[year]['BLACKPINK'] += group2[i]
        years[year]['TWICE'] += group3[i]
        years[year]['Stray Kids'] += group4[i]
        years[year]['NCT 127'] += group5[i]
    
    year = sorted(years.items(), reverse=True)
    return year

def insert_data(cur, conn, year):
    row = cur.execute("SELECT date FROM trends")
    rows = len(row.fetchall())
    max = 25
    if rows < max:
        i = 0
        while i < max:
            if i >= len(year):
                break
            else:
                data = list(year[i])[0]
                group = list(year[i])[1]
                cur.execute("INSERT OR IGNORE INTO trends VALUES(?,?,?,?,?,?,?)", (i+1, data, group['BTS'], group['BLACKPINK'],group['TWICE'],group['Stray Kids'],group['NCT 127']))
                conn.commit()
                i += 1

def main():
    conn, cur = set_connector()
    data = get_data()
    years = set_table(cur, conn, data)
    insert_data(cur, conn, years)

if __name__ == "__main__":
    main()