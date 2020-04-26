import sqlite3
import os
import csv
import matplotlib
import matplotlib.pyplot as plt

def removeDuplicates(lst): 
      
    return list(set([i for i in lst]))
def join_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Stocks_High JOIN Stocks_Low ON Stocks_High.Symbol = Stocks_Low.Symbol")

    return (removeDuplicates(cur.fetchall()))

#print(join_database("stocks_db.sqlite"))

def calculate_net_price(db_lst):

    net_price_lst = []
    for i in db_lst:
        net_price_lst.append((i[0], round(float(i[1]) - float(i[2]), 2), round(float(i[4]) - float(i[5]), 2)))

    return net_price_lst


def write_csv(net_lst, file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path) 

    with open(file_name, 'w') as stock_file:
        write_prices = csv.writer(stock_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_prices.writerow(["Symbol", "Net High Price", "Net Low Price"])

        for i in net_lst:
            write_prices.writerow([i[0], i[1], i[2]])


def create_scatterplot_high_low(net_lst):

    
    for i in net_lst:
        #color_dict = {i[1]: "green", i[2]: "blue"}
        x = i[1]
        y = i[2]
        plt.scatter(x, y)
    
    plt.title("Scatterplot of Net High Prices by Net Low Prices")
    plt.xlabel("Net High Prices: Latest - First Week of 2020")
    plt.ylabel("Net Low Prices: Latest - First Week of 2020")

    plt.savefig("scatterplot_high_low.png")
    plt.show()

def create_scatterplot_symbol_high(net_lst):
    
    for i in net_lst:
        #color_dict = {i[1]: "green", i[2]: "blue"}
        x = i[0]
        y = i[1]
        plt.scatter(x, y)
    
    plt.title("Scatterplot of Stock Symbols by Net High Prices")
    plt.xlabel("Stock Symbols")
    plt.ylabel("Net High Prices: Latest - First Week of 2020")

    plt.savefig("scatterplot_symbol_high.png")

    plt.show()

def create_scatterplot_symbol_low(net_lst):

    for i in net_lst:
        #color_dict = {i[1]: "green", i[2]: "blue"}
        x = i[0]
        y = i[2]
        plt.scatter(x, y)
    plt.title("Scatterplot of Stock Symbols by Net Low Prices")
    plt.xlabel("Stock Symbols")
    plt.ylabel("Net Low Prices: Latest - First Week of 2020")
    
    plt.savefig("scatterplot_symbol_low.png")

    plt.show()


lst = calculate_net_price(join_database("stocks_db.sqlite"))
#print(len(lst))
write_csv(lst, "stocks_net_prices.csv")
create_scatterplot_high_low(lst)
create_scatterplot_symbol_high(lst)
create_scatterplot_symbol_low(lst)