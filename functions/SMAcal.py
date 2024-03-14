import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go


def calculate_sma(data):
    data['Datetime']=pd.to_datetime(data['Datetime'])
    data1=data.set_index('Datetime')
    # Simple Moving Average (SMA)
    data1['2_SMA'] = data1['Close'].rolling(window=2).mean() #trung binh cua 2 gtri lien tiep
    data1['5_SMA'] = data1['Close'].rolling(window=5).mean() #trung binh cua 5 gtri lien tiep
    data1 = data1[data1['5_SMA'].notna()]
    return data1

def SMA_tradecalls(data):
    Trade_Buy=[]
    Trade_Sell=[]
    data1=calculate_sma(data)
    for i in range(len(data1)-1):
        if ((data1['2_SMA'].values[i] < data1['5_SMA'].values[i]) & (data1['2_SMA'].values[i+1] > data1['5_SMA'].values[i+1])):
            print("Trade Call for {row} is Buy.".format(row=data1.index[i].date()))
            Trade_Buy.append(i)
        elif ((data1['2_SMA'].values[i] > data1['5_SMA'].values[i]) & (data1['2_SMA'].values[i+1] < data1['5_SMA'].values[i+1])):
            print("Trade Call for {row} is Sell.".format(row=data1.index[i].date()))
            Trade_Sell.append(i)
    return Trade_Buy, Trade_Sell

# Visualizing SMA trade calls
def plot_SMA_tradecalls(data,Trade_Buy,Trade_Sell):
    data1 = calculate_sma(data)
    data2 = data1.reset_index()
    Trade_Buy, Trade_Sell = SMA_tradecalls(data)
    st.markdown("<h2 style='text-align: center;'>SMA generated signals</h2>", unsafe_allow_html=True)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data2['Datetime'], y=data2['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data2['Datetime'], y=data2['2_SMA'], mode='lines', name='2_SMA', line=dict(color='green', width=1)))
    fig.add_trace(go.Scatter(x=data2['Datetime'], y=data2['5_SMA'], mode='lines', name='5_SMA', line=dict(color='red', width=1)))
    fig.add_trace(go.Scatter(x=data2.loc[Trade_Buy, 'Datetime'], y=data2.loc[Trade_Buy, '2_SMA'], mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='green', size=7, line=dict(width=0.3))))
    fig.add_trace(go.Scatter(x=data2.loc[Trade_Sell,  'Datetime'], y=data2.loc[Trade_Sell, '5_SMA'], mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=7, line=dict(width=0.3))))

    fig.update_layout(xaxis_title='Date', yaxis_title='Price in Dollars') 
                          #plot_bgcolor='rgb(224, 224, 224)') #height=600, width=1100)
    fig.update_xaxes(showgrid=True, gridwidth=0.5)# gridcolor='White')
    fig.update_yaxes(showgrid=True, gridwidth=0.5)#, gridcolor='White')

    st.plotly_chart(fig)
