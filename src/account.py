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

print(preProcessedTransaction_df.head())

def processTransaction(pPTransaction_df):
    df = pPTransaction_df.copy()
    df = df.drop(['trans_id'], axis=1)

    # Get several GroupBy Objects
    gb = df.groupby(['account_id'])
    gb_type = df.groupby(['account_id', 'type'])
    gb_year = df.groupby(['account_id', 'year'])
    gb_type_year = df.groupby(['account_id', 'type', 'year'])
    
    # Get statistics for balance after each transaction
    balance_all = gb.agg({'balance': ['mean', 'min', 'max']}).droplevel(1, axis=1).set_axis(['balance_mean', 'balance_min', 'balance_max'], axis=1)
    
    # Get statistics for number of transactions of each type
    no_of_type_transactions = gb_type.size().to_frame().reset_index().pivot(index='account_id', columns='type').droplevel(['type'], axis=1).set_axis(['debits', 'credits'], axis=1)
    
    # Get statistics for transaction amount and balance after transaction for each type
    amount_balance_type = gb_type.agg({'amount': ['sum', 'mean', 'min', 'max'], 'balance': ['mean', 'min', 'max']}).reset_index().pivot(index='account_id', columns='type').droplevel([0, 'type'], axis=1).set_axis(['amount_sum_debit', 'amount_sum_credit', 'amount_mean_debit', 'amount_mean_credit', 'amount_min_debit', 'amount_min_credit', 'amount_max_debit', 'amount_max_credit', 'balance_mean_debit', 'balance_mean_credit', 'balance_min_debit', 'balance_min_credit', 'balance_max_debit', 'balance_max_credit'], axis=1)
    
    # Get new dataframe with number of transactions for each account
    counts = gb.size().to_frame(name='no. of transactions')
    
    # Join all the data for each account
    counts = counts.join(balance_all).join(no_of_type_transactions).join(amount_balance_type).reset_index()
    
    # TODO stats per year
    # TODO stats per type per year
    
    return counts
    
processedTransaction_df = processTransaction(preProcessedTransaction_df)

print(processedTransaction_df)