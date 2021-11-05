import pandas as pd
import os
from csv import reader

# the number is in the form YYMMDD for men,
# the number is in the form YYMM+50DD for women,

#os.system('cls' if os.name == 'nt' else 'clear')

def toGender(birth_number):
    #year = birth_number // 10000
    month = (birth_number // 100) % 100
    #day = birth_number % 100
    #year = str(year).zfill(2)
    #day = str(day).zfill(2)
    
    if (month > 50):
        gender = 'F'
        #month = str(month-50).zfill(2)
    else:
        gender = 'M'
        #month = str(month).zfill(2)
    
    return gender

client_fields = ['client_id', 'birth_number', 'district_id']
clients = pd.read_csv('data/client.csv', usecols=client_fields, sep=';')
clients = pd.DataFrame(clients)

print(type(clients.birth_number))
#clients['gender'] = 'F' if ((clients.birth_number // 100) % 100) > 50 else 'M'


print("HEAD\n", clients.head(), "\n")
#print("INFO\n", clients.info(), "\n")
#print("DESCRIBE\n", clients.describe(), "\n")