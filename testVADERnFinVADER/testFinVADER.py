from finvader import finvader  
import numpy as np
import pandas as pd

text = "The period's sales dropped to EUR 30.6 m from EUR 38.3 m, according to the interim report, released today."

scores = finvader(text, 
                  use_sentibignomics = True, 
                  use_henry = True, 
                  indicator = 'compound' )
print(scores)

data = pd.read_csv('financial_phrasebank.csv',index_col=None)
                       
data['finvader'] = data['sentence'].apply(finvader,use_sentibignomics = True, use_henry = True, indicator="compound")
print(data.head()) 