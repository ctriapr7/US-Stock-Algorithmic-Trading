import pandas as pd
import numpy as np
from pandas_datareader import data as web
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt

start = dt.datetime(2016, 1, 2)
end = dt.datetime(2022, 8, 29)

stock_name=input("Enter the stock symbol of your firm (capitalized): ")
stock_name = stock_name.upper()

stock = web.DataReader(stock_name, 'yahoo', start, end)
SMA30=pd.DataFrame()
SMA30['Adj Close']=stock['Adj Close'].rolling(30).mean()

SMA100=pd.DataFrame()
SMA100['Adj Close']=stock['Adj Close'].rolling(100).mean()

plt.figure(figsize=(15, 5))
plt.plot(stock['Adj Close'], label=stock_name)
plt.plot(SMA30['Adj Close'], label="SMA30")
plt.plot(SMA100['Adj Close'], label="SMA100")
plt.xlabel("Jan 2016- Aug 2022")
plt.ylabel("Adj Close Prices in USD")
plt.legend(loc="upper left")
plt.show()

stock_data = pd.DataFrame()
stock_data['Stock'] = stock['Adj Close']
stock_data['SMA30'] = SMA30['Adj Close']
stock_data['SMA100'] = SMA100['Adj Close']
print(stock_data.tail(5))

#function to create signals for buying and selling
def signalStock(data):
    signalBuyPrice=[]
    signalSellPrice=[]
    flag = -1 #if flag is 1, a buy is recently conducted, or if flag is 0, a sell is recently conducted. Use -1 to start

    for i in range(len(data)):
        if data['SMA30'][i]> data['SMA100'][i]: #when short term SMA crosses above long term SMA, BUY
            if flag!=1:
                signalBuyPrice.append(stock_data['Stock'][i])
                signalSellPrice.append(np.nan)
                flag=1
            else:
                signalBuyPrice.append(np.nan)
                signalSellPrice.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]: #when short term SMA crosses above long term SMA, BUY
            if flag!=0:
                signalSellPrice.append(stock_data['Stock'][i])
                signalBuyPrice.append(np.nan)
                flag=0
            else:
                signalBuyPrice.append(np.nan)
                signalSellPrice.append(np.nan)
        else:
            signalBuyPrice.append(np.nan)
            signalSellPrice.append(np.nan)
    return(signalBuyPrice, signalSellPrice)

signal = signalStock(stock_data)

stock_data['Buy_Signal_Price'] = signal[0]
stock_data['Sell_Signal_Price']= signal[1]

plt.figure(figsize=(15,5))
plt.plot(stock_data['Stock'],label = 'FB', alpha = 0.30)
plt.plot(stock_data['SMA30'], label = 'SMA30', alpha = 0.30)
plt.plot(stock_data['SMA100'], label = 'SMA100', alpha = 0.30)
plt.scatter(stock_data.index,stock_data['Buy_Signal_Price'], label = 'Buy', marker = '^', color = 'green')
plt.scatter(stock_data.index,stock_data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
plt.legend(loc='upper left')
plt.show()






