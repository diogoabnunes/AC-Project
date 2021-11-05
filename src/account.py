import pandas as pd
import matplotlib.pyplot as plt

account_fields = ['account_id', 'district_id', 'frequency', 'date']
accounts = pd.read_csv('../data/account.csv', usecols=account_fields, sep=';')

loan_fields = ['loan_id', 'account_id', 'date', 'amount', 'duration', 'payments', 'status']
loans = pd.read_csv('../data/loan_train.csv', usecols=loan_fields, sep=';')

accounts_loans = pd.merge(accounts, loans, how='inner', on='account_id').groupby(by='account_id')

print(accounts_loans)