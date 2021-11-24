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
    gb_year_type = df.groupby(['account_id', 'year', 'type'])
    
    # Get statistics for balance after each transaction
    balance_all = gb.agg({'balance': ['mean', 'min', 'max']}).droplevel(1, axis=1).set_axis(['balance_mean', 'balance_min', 'balance_max'], axis=1)
    
    # Get statistics for number of transactions of each type
    no_of_type_transactions = gb_type.size().to_frame().reset_index().pivot(index='account_id', columns='type').droplevel(['type'], axis=1).set_axis(['debits', 'credits'], axis=1)
    
    # Get statistics for transaction amount and balance after transaction for each type
    amount_balance_type = gb_type.agg({'amount': ['sum', 'mean', 'min', 'max'], 'balance': ['mean', 'min', 'max']}).reset_index().pivot(index='account_id', columns='type').droplevel([0, 'type'], axis=1).set_axis(['amount_sum_debit', 'amount_sum_credit', 'amount_mean_debit', 'amount_mean_credit', 'amount_min_debit', 'amount_min_credit', 'amount_max_debit', 'amount_max_credit', 'balance_mean_debit', 'balance_mean_credit', 'balance_min_debit', 'balance_min_credit', 'balance_max_debit', 'balance_max_credit'], axis=1)
    
    # Get statistics for number of transactions of each year
    no_of_year_transactions = gb_year.size().to_frame().reset_index().pivot(index='account_id', columns='year').droplevel(['year'], axis=1).set_axis(['no. of transactions 1993', 'no. of transactions 1994', 'no. of transactions 1995', 'no. of transactions 1996'], axis=1).fillna(0)
    
    # Get statistics for balance after transaction for each year
    balance_all_year = gb_year.agg({'balance': ['mean', 'min', 'max']}).reset_index().pivot(index='account_id', columns='year').droplevel([0, 1], axis=1).set_axis(['balance_mean_1993', 'balance_mean_1994', 'balance_mean_1995', 'balance_mean_1996', 'balance_min_1993', 'balance_min_1994', 'balance_min_1995', 'balance_min_1996', 'balance_max_1993', 'balance_max_1994', 'balance_max_1995', 'balance_max_1996'], axis=1)
    
    # Get statistics for number of transactions of each type in each year
    no_of_year_type_transactions = gb_year_type.size().to_frame().reset_index().pivot(index='account_id', columns=['year', 'type']).droplevel([0, 1], axis=1).set_axis(['1995_debits', '1995_credits', '1996_debits', '1996_credits', '1993_debits', '1993_credits', '1994_debits', '1994_credits'], axis=1)
    
    # Get statistics for transaction amount and balance after transaction for each type in each year
    amount_balance_year_type = gb_year_type.agg({'amount': ['sum', 'mean', 'min', 'max'], 'balance': ['mean', 'min', 'max']}).reset_index().pivot(index='account_id', columns=['year', 'type']).droplevel([0, 1], axis=1).set_axis(['amount_sum_1993_debit', 'amount_sum_1993_credit', 'amount_sum_1994_debit', 'amount_sum_1994_credit', 'amount_sum_1995_debit', 'amount_sum_1995_credit', 'amount_sum_1996_debit', 'amount_sum_1993_credit', 'amount_mean_1993_debit', 'amount_mean_1993_credit', 'amount_mean_1994_debit', 'amount_mean_1994_credit', 'amount_mean_1995_debit', 'amount_mean_1995_credit', 'amount_mean_1996_debit', 'amount_mean_1996_credit', 'amount_min_1993_debit', 'amount_min_1993_credit', 'amount_min_1994_debit', 'amount_min_1994_credit', 'amount_min_1995_debit', 'amount_min_1995_credit', 'amount_min_1996_debit', 'amount_min_1996_credit', 'amount_max_1993_debit', 'amount_max_1993_credit', 'amount_max_1994_debit', 'amount_max_1994_credit', 'amount_max_1995_debit', 'amount_max_1995_credit', 'amount_max_1996_debit', 'amount_max_1996_credit', 'balance_mean_1993_debit', 'balance_mean_1993_credit', 'balance_mean_1994_debit', 'balance_mean_1994_credit', 'balance_mean_1995_debit', 'balance_mean_1995_credit', 'balance_mean_1996_debit', 'balance_mean_1996_credit', 'balance_min_1993_debit', 'balance_min_1993_credit', 'balance_min_1994_debit', 'balance_min_1994_credit', 'balance_min_1995_debit', 'balance_min_1995_credit', 'balance_min_1996_debit', 'balance_min_1996_credit', 'balance_max_1993_debit', 'balance_max_1993_credit', 'balance_max_1994_debit', 'balance_max_1994_credit', 'balance_max_1995_debit', 'balance_max_1995_credit', 'balance_max_1996_debit', 'balance_max_1996_credit'], axis=1)
    
    # Get new dataframe with number of transactions for each account
    counts = gb.size().to_frame(name='no. of transactions')
    
    # Join all the data for each account
    counts = counts.join(balance_all).join(no_of_type_transactions).join(amount_balance_type).join(no_of_year_transactions).join(balance_all_year).join(no_of_year_type_transactions).join(amount_balance_year_type).reset_index()
    
    return counts
    
processedTransaction_df = processTransaction(preProcessedTransaction_df)

print(processedTransaction_df)