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
    return date_list, total_list

def main():
    conn, cur = set_connector()
    date_list, total_list = kpop_growth('trend_calculation.txt', cur, conn)
    
if __name__ == "__main__":
    main()