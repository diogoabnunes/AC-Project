import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

def csv_df(file, **kwargs):
    return pd.read_csv(file, sep=kwargs.pop('sep', ';'), na_values=kwargs.pop('na_values', None), dtype=kwargs.pop('dtype', None))

transaction_df = csv_df('../data/trans_train.csv', dtype={'bank': str})
 
def preProcessTransaction(transaction_df):
    df = transaction_df.copy()
    
    # Splitting loan grant date
    df['year'] = 1900 + (df['date'] // 10000) # get first 2 digits
    df['day'] = df['date'] % 100 # get last 2 digits
    df['month'] = (df['date'] % 10000) // 100 # get middle digits
    
    # Replacing values in type column
    df['type'].replace({'credit': 1, 'withdrawal': -1, 'withdrawal in cash': -1}, inplace=True)
    
    # Removing unnecessary columns
    df = df.drop(['date', 'day', 'bank', 'account', 'operation', 'k_symbol'], axis=1)
    
    return df

preProcessedTransaction_df = preProcessTransaction(transaction_df)

def processTransaction(pPTransaction_df):
    df = pPTransaction_df.copy()
    df = df.drop(['trans_id'], axis=1)

    gk = df.groupby(['account_id'])
    
    counts = gk.size().to_frame(name='counts')
    
    #counts.join(gk.agg({}))
    
    return counts
    
processedTransaction_df = processTransaction(preProcessedTransaction_df)

print(processedTransaction_df.head())