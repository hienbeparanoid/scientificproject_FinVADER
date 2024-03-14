import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# data_tsla = pd.read_csv('functions/data/data_tsla.csv')
# data_tsla['Datetime'] = pd.to_datetime(data_tsla['Datetime'])
# data_tsla = data_tsla.set_index('Datetime')

# cmt_data = pd.read_csv('functions/data/tsla_merged.csv')


def show_hide_stockdata_button(data):
    #global data_tsla
    if st.session_state['show_data']:
        st.dataframe(data)

def show_hide_cmtdata_button(data):
    #global cmt_data
    # Hiển thị dữ liệu nếu biến phiên là True
    if st.session_state['show_data']:
        st.dataframe(data)

def stockdata_chart(data):
    #global data_tsla
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data = data.set_index('Datetime')
    st.markdown("<h2 style='text-align: center;'>Price fluctuations</h2>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    st.plotly_chart(fig)