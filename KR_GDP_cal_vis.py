import sqlite3
import matplotlib.pyplot as plt

def set_connector():
    '''Set the connector and cursor'''

    conn = sqlite3.connect('K-POP.db')
    cur = conn.cursor()
    return conn, cur

def gdp_growth(filename, cur, conn):
    '''Calculate the winning rate of home teams'''

    cur.execute("SELECT date FROM gdp")
    conn.commit()
    date = cur.fetchall()
    j = 0
    date_list = []
    while j < len(date):
        for l in date[j]:
            date_list.append(l)
        j += 1

    cur.execute("SELECT value FROM gdp")
    conn.commit()
    value = cur.fetchall()
    i = 0
    y = 0
    int_gdp = []
    gdp_difference = []
    while i < len(value):
        for x in value[i]:
            int_gdp.append(x)
        i += 1
    int_gdp.reverse()
    
    f = open(filename, 'w')
    f.write("Calculate the gdp changes from 1960 to 2021 comparing the gdp of two consecutive years\n")
    f.write("Simply subtract the gdp of first year from second year\n")
    f.write("---------------------------------------------------------------------------------------------------------\n")
    
    while y < len(int_gdp)-1:
        diff = int_gdp[y] - int_gdp[y+1]
        gdp_difference.append(diff)
        f.write("The gdp difference between "+date_list[y]+" and "+date_list[y+1]+" is ...  ")
        f.write(str(int_gdp[y])+" - "+str(int_gdp[y+1])+" = "+str(diff)+"\n")
        y += 1
    return date_list, gdp_difference

def visualization(date, gdp_difference):
    '''Create Line Graph'''
    
    i = 0
    middle_year = []
    while i < len(date)-1:
        middle = (int(date[i+1]) + int(date[i])) / 2
        middle_year.append(middle)
        i += 1

    plt.figure()
    plt.plot(middle_year, gdp_difference)
    plt.xlabel("YEAR")
    plt.ylabel("GDP")
    plt.title("GDP changes over time")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.show()

def main():
    conn, cur = set_connector()
    date_list, gdp_difference = gdp_growth('gdp_calculation.txt', cur, conn)
    visualization(date_list, gdp_difference)
    
if __name__ == "__main__":
    main()