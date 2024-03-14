import streamlit as st
import pandas as pd
import numpy as np
import functions.showinputdata_button
import functions.SMAcal
import functions.finVADERcal
import time
import functions.backtest
import webbrowser
import os
import pathlib

def open_html_file(file_name):
    # Lấy đường dẫn tới thư mục hiện tại của script Python
    html_file_path = pathlib.Path(file_name).absolute().as_uri()
    webbrowser.open( html_file_path)

st.set_page_config(page_title='FinVADER - Stockapp',page_icon="💹", layout="wide")
st.title("FinVADER in Stock application")
st.write('''This is a website built to evaluate people's sentiments about stock codes, and then generate financial signals in a specified time period.
            This website will provide several options located on the right sidebar.
            You can also see some basic information about the article in the sidebar.
            Enjoy viewing the results of the study, have a nice day!!!!''')
st.write(" ")
st.write(" ")

# Input data
cola , colb = st.columns([1,1])
with cola:
    stock_file=st.file_uploader('Upload a file of stock data')
    if stock_file is not None:
        stock_data=pd.read_csv(stock_file)
    else:
        stock_data=None
with colb:
    text_file=st.file_uploader('Upload a file of social media data')
    if text_file is not None:
        cmt_data=pd.read_csv(text_file)
    else:
        cmt_data=None
st.sidebar.title("Some basic information about the research results")


st.sidebar.caption("Stock code for data")
st.sidebar.code('tsla')
st.sidebar.caption("Data scraping interval")
st.sidebar.code('30/12/2023 - 29/01/2024')

selected_option = st.sidebar.radio('Select your chart requirement',['Price fluctuations',
                                                                    "SMA's chart for price",
                                                                    'finVader value for comment',
                                                                    'Synthesis between SMA and finVader'])
if selected_option == 'Price fluctuations':
    if stock_file is not None:
        df=stock_data.copy()
        functions.showinputdata_button.stockdata_chart(df)
if selected_option == "SMA's chart for price":
    df2 = stock_data.copy()
    df22 = functions.SMAcal.calculate_sma(df2)
    Trade_Buy , Trade_Sell = functions.SMAcal.SMA_tradecalls(df2)
    functions.SMAcal.plot_SMA_tradecalls(df2,Trade_Buy,Trade_Sell)
    col1, col2 = st.columns([2,1])
    with col1:
        st.write("")
    with col2:
        if st.button('View in a detailed mode 👉'):
            st.session_state['show_data'] = not st.session_state.get('show_data', False)
            #html_file_name = 'SMACrosss.html'
            # Mở tệp HTML
            #open_html_file(html_file_name)
            webbrowser.open('D:/#ICARE_BACKUP 12.11.22/Documents/Code/NCKH/semifinal/SMACrosss.html')
if selected_option == 'finVader value for comment':
    functions.finVADERcal.plot_finvader_tradecalls()
if selected_option == 'Synthesis between SMA and finVader':
    functions.finVADERcal.finvadernSMA()
    col1, col2 = st.columns([2,1])
    with col1:
        st.write("")
    with col2:
        if st.button('View in a detailed mode 👉'):
            st.session_state['show_data'] = not st.session_state.get('show_data', False)
            html_file_name = 'finVADERnSMA1.html'
            # Mở tệp HTML
            #open_html_file(html_file_name)
            webbrowser.open('D:/#ICARE_BACKUP 12.11.22/Documents/Code/NCKH/semifinal/finVADERnSMA1.html')

st.sidebar.write('Would you like to evaluate the performance?')
if st.sidebar.checkbox('Yes'):
    if selected_option == "SMA's chart for price":
        functions.backtest.backtest_sma()
    if selected_option == 'Synthesis between SMA and finVader':
        functions.backtest.backtest_finvader()

st.sidebar.caption("Input Data for show")

if st.sidebar.button('Stock data',key='stockdata'):
    st.session_state['show_data'] = not st.session_state.get('show_data', False)
    if stock_data is None:
        st.write('No data to show')
    else:
        st.dataframe(stock_data)

if st.sidebar.button('Social media data',key='cmtdata'):
    st.session_state['show_data'] = not st.session_state.get('show_data', False)
    if cmt_data is None:
        st.write('No data to show')
    else:
        st.dataframe(cmt_data)

st.success('Hope you will make high profits!!!')
if 'balloons_shown' not in st.session_state:
    st.balloons()
    st.session_state['balloons_shown'] = True

