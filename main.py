import pandas as pd
import numpy as np
from pandas_datareader import data as web
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt

start = dt.datetime(2016, 1, 2)
end = dt.datetime(2022, 8, 29)

stock_name=input("Enter the stock symbol of your firm: ")
stock_name = stock_name.upper()

stock = web.DataReader(stock_name, 'yahoo', start, end)
SMA50=pd.DataFrame()
SMA50['Adj Close']=stock['Adj Close'].rolling(50).mean()

SMA200=pd.DataFrame()
SMA200['Adj Close']=stock['Adj Close'].rolling(200).mean()

plt.figure(figsize=(15, 5))
plt.plot(stock['Adj Close'], label=stock_name)
plt.plot(SMA50['Adj Close'], label="SMA50")
plt.plot(SMA200['Adj Close'], label="SMA100")
plt.xlabel("Jan 2016- Aug 2022")
plt.ylabel("Adj Close Prices in USD")
plt.legend(loc="upper left")
plt.show()

stock_data = pd.DataFrame()
stock_data['Stock'] = stock['Adj Close']
stock_data['SMA50'] = SMA50['Adj Close']
stock_data['SMA200'] = SMA200['Adj Close']

#function to create signals for buying and selling
def signalStock(data):
    signalBuyPrice=[]
    signalSellPrice=[]
    flag = -1 #if flag is 1, a buy is recently conducted, or if flag is 0, a sell is recently conducted. Use -1 to start

    for i in range(len(data)):
        if data['SMA50'][i]> data['SMA200'][i]: #when short term SMA crosses above long term SMA, BUY
            if flag!=1:
                signalBuyPrice.append(stock_data['Stock'][i])
                signalSellPrice.append(np.nan)
                flag=1
            else:
                signalBuyPrice.append(np.nan)
                signalSellPrice.append(np.nan)
        elif data['SMA50'][i] < data['SMA200'][i]: #when short term SMA crosses above long term SMA, BUY
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
plt.plot(stock_data['Stock'],label = stock_name, alpha = 0.30)
plt.plot(stock_data['SMA50'], label = 'SMA50', alpha = 0.30)
plt.plot(stock_data['SMA200'], label = 'SMA200', alpha = 0.30)
plt.xlabel("Jan 2016 - Aug 2022")
plt.ylabel("Prices in USD")
plt.scatter(stock_data.index,stock_data['Buy_Signal_Price'], label = 'Buy', marker = '^', color = 'green')
plt.scatter(stock_data.index,stock_data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
plt.legend(loc='upper left')
plt.show()
print(stock_data)





