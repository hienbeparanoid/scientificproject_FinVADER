from datasets import load_dataset
import pandas as pd

dataset = load_dataset("financial_phrasebank",'sentences_50agree')
# Convert to Pandas DataFrame
df = pd.DataFrame(dataset['train'])  # Use 'test' or 'validation' if needed

# Save the DataFrame to a CSV file
df.to_csv('financial_phrasebank.csv', index=False)