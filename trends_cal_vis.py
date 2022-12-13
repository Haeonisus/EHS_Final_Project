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


def trend_visualization(year, cur, conn):
    cur.execute("SELECT BTS FROM trends")
    conn.commit()
    bts = cur.fetchall()
    bts_list = []
    i = 0
    while i < len(bts):
        btsRow = sum(bts[i])
        bts_list.append(btsRow)
        i += 1
    bts_list.reverse()

    cur.execute("SELECT BLACKPINK FROM trends")
    conn.commit()
    bp = cur.fetchall()
    bp_list = []
    i = 0
    while i < len(bp):
        bpRow = sum(bp[i])
        bp_list.append(bpRow)
        i += 1
    bp_list.reverse()

    cur.execute("SELECT TWICE FROM trends")
    conn.commit()
    twice = cur.fetchall()
    twice_list = []
    i = 0
    while i < len(twice):
        twiceRow = sum(twice[i])
        twice_list.append(twiceRow)
        i += 1
    twice_list.reverse()

    cur.execute("SELECT StrayKids FROM trends")
    conn.commit()
    sk = cur.fetchall()
    sk_list = []
    i = 0
    while i < len(sk):
        skRow = sum(sk[i])
        sk_list.append(skRow)
        i += 1
    sk_list.reverse()

    cur.execute("SELECT NCT127 FROM trends")
    conn.commit()
    nct = cur.fetchall()
    nct_list = []
    i = 0
    while i < len(bp):
        nctRow = sum(nct[i])
        nct_list.append(nctRow)
        i += 1
    nct_list.reverse()

    plt.figure()
    plt.plot(year, bts_list)
    plt.plot(year, bp_list)
    plt.plot(year, twice_list)
    plt.plot(year, sk_list)
    plt.plot(year, nct_list)
    plt.xlabel("YEAR")
    plt.ylabel("Google Trends")
    plt.title("Google search trends changes over time")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.show()


def main():
    conn, cur = set_connector()
    total_list = kpop_growth('trend_calculation.txt', cur, conn)
    total_table(cur, conn, total_list)
    year, gdp, trend = join_table(cur, conn)
    join_visualization(year, gdp, trend)
    trend_visualization(year, cur, conn)
    
if __name__ == "__main__":
    main()