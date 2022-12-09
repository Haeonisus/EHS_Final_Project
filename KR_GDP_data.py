import sqlite3
import requests
import json

def set_connector():
    '''Set the connector and cursor'''

    conn = sqlite3.connect('K-POP.db')
    cur = conn.cursor()
    return conn, cur

def get_data():
    '''Get the data and store it in json format'''
    
    data = []
    page = [1, 2]
    for i in page:
        url = f"http://api.worldbank.org/v2/country/KR/indicator/NY.GDP.MKTP.CD?format=json&page={i}"
        response = requests.get(url)
        content = json.loads(response.text)[1]
        data.append(content)
    return data

def set_table(cur, conn, content):
    '''Set the table'''

    #cur.execute('''DROP TABLE IF EXISTS gdp''')
    cur.execute('''CREATE TABLE IF NOT EXISTS gdp(id INTEGER PRIMARY KEY, date TEXT, value INTEGER)''')
    conn.commit()

    date = []
    value = []
    for i in content:
        for item in i:
            date.append(item['date'])
            value.append(int(item['value']))
    return date, value

def insert_data(cur, conn, date, value):
    '''Insert the data into the table'''

    row = cur.execute("SELECT date FROM gdp")
    rows = len(row.fetchall())
    max = 25
    if rows < max:
        i = 0
        while i < max:
            cur.execute("INSERT OR IGNORE INTO gdp VALUES(?,?,?)", (i+1, date[i], value[i]))
            conn.commit()
            i += 1
    if rows >= max and rows < rows+max:
        i = 25
        while i < max+max:
            cur.execute("INSERT OR IGNORE INTO gdp VALUES(?,?,?)", (i+1, date[i], value[i]))
            conn.commit()
            i += 1
    if rows >= max+max:
        i = 50
        while i < max+max+max:
            if i >= len(date):
                break
            else:
                cur.execute("INSERT OR IGNORE INTO gdp VALUES(?,?,?)", (i+1, date[i], value[i]))
                conn.commit()
                i += 1

def main():
    conn, cur = set_connector()
    data = get_data()
    date, value = set_table(cur, conn, data)
    insert_data(cur, conn, date, value)

if __name__ == "__main__":
    main()