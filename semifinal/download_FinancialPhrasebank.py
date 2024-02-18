from datasets import load_dataset
import pandas as pd

dataset = load_dataset("financial_phrasebank",'sentences_50agree')
# Convert to Pandas DataFrame
df = pd.DataFrame(dataset['train'])  # Use 'test' or 'validation' if needed
df['label'] = df['label'].replace({1: 0, 0: -1, 2: 1})
df['label'] = df['label'].to_f
print(df)
# Save the DataFrame to a CSV file
df.to_csv('financial_phrasebank.csv', index=False)