import pandas as pd
import os

#os.system('cls' if os.name == 'nt' else 'clear')

client_fields = ['client_id', 'birth_number', 'district_id', 'gender']
clients = pd.read_csv('data/updatedClient.csv', usecols=client_fields, sep=',')
clients_df = pd.DataFrame(clients)

print("HEAD\n", clients_df.head(), "\n")
print("INFO\n", clients_df.info(), "\n")
print("DESCRIBE\n", clients_df.describe(), "\n")