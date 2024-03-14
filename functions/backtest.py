from backtesting.test import SMA
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from backtesting import Backtest
from backtesting import Strategy
import streamlit as st

#BACKTEST FINVADER + SMA
# 2 list chứa index là tín hiệu sell/buy của df data_tsla, lấy ở kq bên finvader_analysis4_preprocess.py
final_buy = [130, 4, 135, 12, 17, 147, 22, 157, 29, 36, 42, 47, 175, 51, 188, 64, 71, 80, 213, 93, 227, 107, 111, 119]
final_sell = [0, 132, 5, 140, 16, 18, 152, 26, 30, 38, 166, 44, 49, 180, 60, 67, 196, 73, 203, 85, 220, 99, 108, 116, 122]

stock = pd.read_csv('functions/data/data_tsla.csv')
# Initialize the 'signal' column with 0
stock['signal'] = 0
# Set 'signal' to 1 for the indices in 'final_buy'
stock.loc[stock.index.isin(final_buy), 'signal'] = 1
# Set 'signal' to 0 for the indices in 'final_sell'
stock.loc[stock.index.isin(final_sell), 'signal'] = -1
stock.to_csv('functions/data/stock.csv')

class finVADERnSMA(Strategy):
    def init(self):
        pass

    def next(self):
        signal = self.data.signal[-1]
        if signal == 1:
            self.position.close()
            self.buy()
        elif signal == -1:
            self.position.close()
            self.sell()
# Sử dụng Backtest với dữ liệu mới
stockk=pd.read_csv('functions/data/stock.csv', index_col='Datetime', parse_dates=True)
bt = Backtest(stockk, finVADERnSMA, cash=100000, commission=.002)
stat = bt.run()

#BACKTEST SMA
# 2 list chứa index là tín hiệu sell/buy của df data_tsla, lấy ở kq bên scrapestockdata.py
Trade_Buy=[4, 12, 17, 22, 29, 36, 42, 47, 51, 64, 71, 80, 93, 107, 111, 119, 130, 135, 147, 157, 175, 188, 213, 227]
Trade_Sell=[0, 5, 16, 18, 26, 30, 38, 44, 49, 60, 67, 73, 85, 99, 108, 116, 122, 132, 140, 152, 166, 180, 196, 220]

stock1 = pd.read_csv('functions/data/data_tsla.csv')
# Initialize the 'signal' column with 0
stock1['signal'] = 0
# Set 'signal' to 1 for the indices in 'final_buy'
stock1.loc[stock1.index.isin(Trade_Buy), 'signal'] = 1
# Set 'signal' to 0 for the indices in 'final_sell'
stock1.loc[stock1.index.isin(Trade_Sell), 'signal'] = -1
stock1.to_csv('functions/data/stock1.csv')

class SMA(Strategy):
    def init(self):
        pass

    def next(self):
        signal = self.data.signal[-1]
        if signal == 1:
            self.position.close()
            self.buy()     
        elif signal == -1:
            self.position.close()
            self.sell()

# Sử dụng Backtest với dữ liệu mới
stock1=pd.read_csv('functions/data/stock1.csv', index_col='Datetime', parse_dates=True)
bt1 = Backtest(stock1, SMA, cash=100000, commission=.002)
stat1 = bt1.run()

def backtest_finvader():
    global stat
    st.markdown("<h2>BACKTEST index</h2>", unsafe_allow_html=True)
    st.text(stat)

def backtest_sma():
    global stat1
    st.markdown("<h2>BACKTEST index</h2>", unsafe_allow_html=True)
    st.text(stat1)
