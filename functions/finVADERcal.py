import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from finvader import finvader
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go

data_tsla=pd.read_csv('functions/data/data_tsla_SMA.csv')
Trade_Buy = [4, 12, 17, 22, 29, 36, 42, 47, 51, 64, 71, 80, 93, 107, 111, 119, 130, 135, 147, 157, 175, 188, 213, 227]
Trade_Sell = [0, 5, 16, 18, 26, 30, 38, 44, 49, 60, 67, 73, 85, 99, 108, 116, 122, 132, 140, 152, 166, 180, 196, 220]

# preprocess data
df = pd.read_csv('functions/data/tsla_merged.csv')
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= '2024-01-01']
df = df.drop_duplicates(subset='comment_text')
def clean(text):
# Removes all special characters and numericals leaving the alphabets
    text = re.sub('[^A-Za-z]+', ' ', text)
    return text

# Cleaning the text in the review column
df['cleaned comment_text'] = df['comment_text'].apply(clean)
# Load the English stopwords
stop_words = set(stopwords.words('english'))

# Function to remove stopwords from a text
nltk.download('stopwords')
nltk.download('punkt')
def remove_stopwords(text):
    text = str(text)
    word_tokens = word_tokenize(text)  # Tokenize the text into words
    filtered_sentence = [word for word in word_tokens if word.casefold()  not in stop_words]  # Remove stopwords
    return ' '.join(filtered_sentence)  # Join the words back into a sentence

df['no_sw_cmt'] = df['cleaned comment_text'].apply(remove_stopwords)
df = df[~(df.apply(lambda row: (row == 'deleted').all(), axis=1))]

tsla_cleaned = df

# apply finVADER calculation

news_df = tsla_cleaned

final_news = news_df.loc[:,['date','no_sw_cmt']]
final_news['date'] = pd.to_datetime(final_news['date'])
final_news.sort_values(by='date',inplace=True)

# Import BDay to determine business day's dates
from pandas.tseries.offsets import BDay

# to get the business day for which particular news headline should be used to make trade calls
def get_trade_open(date):
    curr_date_open = pd.to_datetime(date).floor('d').replace(hour=13,minute=30) - BDay(0)
    curr_date_close = pd.to_datetime(date).floor('d').replace(hour=20,minute=0) - BDay(0)
    
    prev_date_close = (curr_date_open - BDay()).replace(hour=20,minute=0)
    next_date_open = (curr_date_close + BDay()).replace(hour=13,minute=30)
    
    if ((pd.to_datetime(date)>=prev_date_close) & (pd.to_datetime(date)<curr_date_open)):
        return curr_date_open
    elif ((pd.to_datetime(date)>=curr_date_close) & (pd.to_datetime(date)<next_date_open)):
        return next_date_open
    else:
        return None

 # Apply the above function to get the trading time for each news headline
final_news["trading_time"] = final_news["date"].apply(get_trade_open)

final_news = final_news[pd.notnull(final_news['trading_time'])]
final_news['Date'] = pd.to_datetime(pd.to_datetime(final_news['trading_time']).dt.date)
final_news['no_sw_cmt'] = final_news['no_sw_cmt'].astype(str)
final_news['compound_finvader_score'] = final_news['no_sw_cmt'].apply(finvader,use_sentibignomics = True, use_henry = True, indicator="compound")
final_news = final_news[(final_news[['compound_finvader_score']] != 0).all(axis=1)].reset_index(drop=True)

#Retaining extreme (max and min) compound scores for same Day news headlines
unique_dates = final_news['Date'].unique()
grouped_dates = final_news.groupby(['Date'])
keys_dates = list(grouped_dates.groups.keys())

max_cs = []
min_cs = []

for key in grouped_dates.groups.keys():
    data = grouped_dates.get_group(key)
    if data["compound_finvader_score"].max() > 0:
        max_cs.append(data["compound_finvader_score"].max())
    elif data["compound_finvader_score"].max() < 0:
        max_cs.append(0)

    if data["compound_finvader_score"].min() < 0:
        min_cs.append(data["compound_finvader_score"].min())
    elif data["compound_finvader_score"].min() > 0:
        min_cs.append(0)

extreme_scores_dict = {'Date':keys_dates,'max_scores':max_cs,'min_scores':min_cs}
extreme_scores_df = pd.DataFrame(extreme_scores_dict)

#summing and calculating finVader score
final_scores = []
for i in range(len(extreme_scores_df)):
    final_scores.append(extreme_scores_df['max_scores'].values[i] + extreme_scores_df['min_scores'].values[i])

extreme_scores_df['final_scores'] = final_scores

# finVADER trade calls - with threshold
finvader_Buy=[]
finvader_Sell=[]
for i in range(len(extreme_scores_df)):
    if extreme_scores_df['final_scores'].values[i] > 0.33:
        print("Trade Call for {row} is Buy.".format(row=extreme_scores_df['Date'].iloc[i].date()))
        finvader_Buy.append(extreme_scores_df['Date'].iloc[i].date())
    elif extreme_scores_df['final_scores'].values[i] < -0.33:
        print("Trade Call for {row} is Sell.".format(row=extreme_scores_df['Date'].iloc[i].date()))
        finvader_Sell.append(extreme_scores_df['Date'].iloc[i].date())


data_tsla['Datetime'] = pd.to_datetime(data_tsla['Datetime'])
data_tsla1 = data_tsla.set_index('Datetime')
finvader_buy = []
for i in range(len(data_tsla1)):
    if data_tsla1.index[i].date() in finvader_Buy:
        finvader_buy.append(i)

finvader_sell = []
for i in range(len(data_tsla1)):
    if data_tsla1.index[i].date() in finvader_Sell:
        finvader_sell.append(i)

# Visualizing finVADER trade calls

def plot_finvader_tradecalls():
    global data_tsla
    #data_tsla2 = data_tsla1.reset_index()
    global finvader_buy
    global finvader_sell
    st.markdown("<h2 style='text-align: center;'>FinVADER generated signals</h2>", unsafe_allow_html=True)
    fig = go.Figure()    

    fig.add_trace(go.Scatter(x=data_tsla['Datetime'], y=data_tsla['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data_tsla.loc[finvader_buy, 'Datetime'], y=data_tsla.loc[finvader_buy, 'Close'], mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='green', size=7,line=dict(width=0.3))))
    fig.add_trace(go.Scatter(x=data_tsla.loc[finvader_sell, 'Datetime'], y=data_tsla.loc[finvader_sell, 'Close'], mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=7,line=dict(width=0.3))))

    fig.update_layout(xaxis_title='Date', yaxis_title='Price in Dollars') 
                  #plot_bgcolor='rgb(224, 224, 224)', height=600, width=1100)
    fig.update_xaxes(showgrid=True, gridwidth=0.5)
    fig.update_yaxes(showgrid=True, gridwidth=0.5)

    st.plotly_chart(fig)    

# finvader+sma
data_tsla2 = data_tsla.copy()
#data_tsla3 = data_tsla1.reset_index()
data_tsla2['Datetime'] = data_tsla2['Datetime'].dt.date
data_tsla3 = data_tsla2.rename(columns={'Datetime': 'index'})
# Get the 'Datetime' values for each index in 'finvader_buy' and 'finvader_sell'
buy_dates = data_tsla3.loc[finvader_buy, 'index']
sell_dates = data_tsla3.loc[finvader_sell, 'index']

# Drop duplicates, keeping the first occurrence
buy_dates = buy_dates.drop_duplicates(keep='last')
sell_dates = sell_dates.drop_duplicates(keep='last')

# Get the final indices
finvader_buy1 = buy_dates.index
finvader_sell1 = sell_dates.index

finvader_buy1 = finvader_buy1.tolist()
finvader_sell1 = finvader_sell1.tolist()

final_buy = list(set(Trade_Buy + finvader_buy1) - set(Trade_Sell))
final_sell = list(set(Trade_Sell + finvader_sell1) - set(Trade_Buy))

def finvadernSMA():
    global data_tsla
    data_tslaa = data_tsla.reset_index()
    global final_buy
    global final_sell
    st.markdown("<h2 style='text-align: center;'>FinVADER-SMA generated signals</h2>", unsafe_allow_html=True)
    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(x=data_tslaa['Datetime'], y=data_tslaa['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=data_tslaa['Datetime'], y=data_tslaa['2_SMA'], mode='lines', name='2_SMA', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data_tslaa['Datetime'], y=data_tslaa['5_SMA'], mode='lines', name='5_SMA', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data_tslaa.loc[final_buy, 'Datetime'], y=data_tslaa.loc[final_buy, 'Close'], mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='green', size=7,line=dict(width=0.3))))
    fig.add_trace(go.Scatter(x=data_tslaa.loc[final_sell, 'Datetime'], y=data_tslaa.loc[final_sell, 'Close'], mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=7,line=dict(width=0.3))))

    # Set layout properties
    fig.update_layout(
                    #title='Trade Calls - MERGED',
                    xaxis_title='Date',
                    yaxis_title='Price in Dollars',
                    autosize=False,
                    #width=1100,
                    #height=600,
                    #plot_bgcolor='rgb(224, 224, 224)',
            )
    fig.update_xaxes(showgrid=True, gridwidth=0.5)
    fig.update_yaxes(showgrid=True, gridwidth=0.5)

    # Display the figure with Streamlit
    st.plotly_chart(fig)


