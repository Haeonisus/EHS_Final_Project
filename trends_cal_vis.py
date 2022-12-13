import sqlite3
import matplotlib.pyplot as plt

def set_connector():
    '''Set the connector and cursor'''

    conn = sqlite3.connect('K-POP.db')
    cur = conn.cursor()
    return conn, cur

def kpop_growth(filename, cur, conn):
    
    cur.execute("SELECT date FROM trends")
    conn.commit()
    date = cur.fetchall()
    j = 0
    date_list = []
    while j < len(date):
        for l in date[j]:
            date_list.append(l)
        j += 1
    date_list.reverse()

    cur.execute("SELECT BTS, BLACKPINK, TWICE, StrayKids, NCT127 FROM trends")
    conn.commit()
    total = cur.fetchall()
    total_list = []
    i = 0
    while i < len(total):
        totalRow = sum(total[i])
        total_list.append(totalRow)
        i += 1
    total_list.reverse()

    f = open(filename, 'w')
    f.write("Calculate the total search trends per year for all give groups\n")
    f.write("---------------------------------------------------------------------------------------------------------\n")

    y = 0
    while y < len(date_list):
        f.write("The total trend search in " + date_list[y] + " is ... " + str(total_list[y]) + "\n")
        y += 1
    
    total_list.reverse()

    return total_list

def total_table(cur, conn, total_list):
    cur.execute('''CREATE TABLE IF NOT EXISTS totals(id INTEGER PRIMARY KEY, total INTEGER)''')
    conn.commit()
    
    for i in range(len(total_list)):
        cur.execute("INSERT OR IGNORE INTO totals VALUES(?,?)", (i+1, total_list[i]))
        conn.commit()

def join_table(cur, conn):
    cur.execute('''SELECT gdp.date, gdp.value, totals.total FROM totals JOIN gdp ON gdp.id = totals.id''')
    conn.commit()

    s = cur.fetchall()
    conn.commit()
    year = []
    gdp = []
    trend = []
    for i in s:
        year.append(list(i)[0])
        gdp.append(list(i)[1])
        trend.append(list(i)[2] * 500000000)
    year.reverse()
    gdp.reverse()
    trend.reverse()
    return year, gdp, trend

def join_visualization(year, gdp, trend):
    plt.figure()
    plt.plot(year, gdp)
    plt.plot(year, trend)
    plt.xlabel("YEAR")
    plt.ylabel("Growth")
    plt.title("GDP and Trend changes over time")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.show()

def trend_visualization(year, trend):
    pass

def main():
    conn, cur = set_connector()
    total_list = kpop_growth('trend_calculation.txt', cur, conn)
    total_table(cur, conn, total_list)
    year, gdp, trend = join_table(cur, conn)
    join_visualization(year, gdp, trend)
    
if __name__ == "__main__":
    main()