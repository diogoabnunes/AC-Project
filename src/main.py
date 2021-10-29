import pandas as pd

client_fields = ['client_id', 'birth_number', 'district_id']
clients = pd.read_csv('data/client.csv', usecols=client_fields, sep=';')
print(clients.head())

