from datasets import load_dataset
import pandas as pd

df = pd.read_csv('general_financial_news.csv')
df['label'] = df['label'].replace({1: 0, 0: -1, 2: 1})
print(df.dtypes)
print(df)
# Save the DataFrame to a CSV file
df.to_csv('general_financial_news1.csv', index=False)

