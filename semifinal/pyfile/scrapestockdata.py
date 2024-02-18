import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

data_tsla = yf.download(tickers='TSLA', start='2023-12-30', end='2024-1-29', interval='30m')
print(data_tsla)
data_tsla.to_csv('stock_tsla.csv')
#SMA
data_tsla['2_SMA'] = data_tsla['Close'].rolling(window=2).mean() #trung binh cua 2 gtri lien tiep
data_tsla['5_SMA'] = data_tsla['Close'].rolling(window=5).mean() #trung binh cua 5 gtri lien tiep

data_tsla = data_tsla[data_tsla['5_SMA'].notna()]

# SMA trade calls
Trade_Buy=[]
Trade_Sell=[]
for i in range(len(data_tsla)-1):
    if ((data_tsla['2_SMA'].values[i] < data_tsla['5_SMA'].values[i]) & (data_tsla['2_SMA'].values[i+1] > data_tsla['5_SMA'].values[i+1])):
        print("Trade Call for {row} is Buy.".format(row=data_tsla.index[i].date()))
        Trade_Buy.append(i)
    elif ((data_tsla['2_SMA'].values[i] > data_tsla['5_SMA'].values[i]) & (data_tsla['2_SMA'].values[i+1] < data_tsla['5_SMA'].values[i+1])):
        print("Trade Call for {row} is Sell.".format(row=data_tsla.index[i].date()))
        Trade_Sell.append(i)

# Visualizing SMA trade calls
plt.figure(figsize=(20, 10),dpi=80)
plt.plot(data_tsla.index, data_tsla['Close'])
plt.plot(data_tsla.index, data_tsla['2_SMA'],'-^', markevery=Trade_Buy, ms=7, color='green')
plt.plot(data_tsla.index, data_tsla['5_SMA'],'-v', markevery=Trade_Sell, ms=7, color='red')
plt.xlabel('Date',fontsize=14)
plt.ylabel('Price in Dollars', fontsize = 14)
plt.xticks(rotation=60,fontsize=12)
plt.yticks(fontsize=12)
plt.title('Trade Calls - Moving Averages Crossover', fontsize = 16)
plt.legend(['Close','2_SMA','5_SMA'])
plt.grid()
plt.show() 
