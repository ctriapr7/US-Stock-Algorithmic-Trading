import pandas as pd
from pandas_datareader import data as web
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt

start = dt.datetime(2016, 1, 2)
end = dt.datetime(2022, 8, 29)

MT = web.DataReader('META', 'yahoo', start, end)
print()
SMA30=pd.DataFrame()
SMA30['Adj Close']=MT['Adj Close'].rolling(30).mean()

SMA100=pd.DataFrame()
SMA100['Adj Close']=MT['Adj Close'].rolling(100).mean()

plt.figure(figsize=(15,5))
plt.plot(MT['Adj Close'], label="META")
plt.plot(SMA30['Adj Close'], label="SMA30")
plt.plot(SMA100['Adj Close'], label="SMA100")
plt.xlabel("Jan 2016- Aug 2022")
plt.ylabel("Adj Close Prices in USD")
plt.legend(loc="upper left")
plt.show()


#function to create signals for buying and selling
def signalStock(data):
    signalBuyPrice=[]
    signalSellPrice=[]
    flag = -1 #if flag is 1, a buy is recently conducted, or if flag is 0, a sell is recently conducted

    for i in range(len(data)):
