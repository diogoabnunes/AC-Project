import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

def csv_df(file, **kwargs):
    return pd.read_csv(file, sep=kwargs.pop('sep', ';'), na_values=kwargs.pop('na_values', None), dtype=kwargs.pop('dtype', None))

client_df = csv_df('../data/client.csv', dtype={'bank': str})
disp_df = csv_df('../data/disp.csv', dtype={'bank': str})
card_df = csv_df('../data/card_train.csv', dtype={'bank': str})
district_df = csv_df('../data/district.csv', dtype={'bank': str})
 
def preProcessClient(client_df):
    df = client_df.copy()
    
    # Splitting birth_number
    df['year'] = 1900 + (df['birth_number'] // 10000) # get first 2 digits
    df['day'] = df['birth_number'] % 100 # get last 2 digits
    df['mix'] = (df['birth_number'] % 10000) // 100 # get middle digits
    
    # Adding gender column
    df['gender'] = np.where(df['mix'] >= 50, 'F', 'M')
    
    # "Fixing" month, because we already have gender
    df['month'] = np.where(df['mix'] >= 50, df['mix'] - 50, df['mix'])
    
    # Renaming birth_number column to birth
    df['birth_number'] = df['year']*10000 + df['month']*100 + df['day']
    df['birth'] = pd.to_datetime(df['birth_number'], format='%Y%m%d')
    
    # Removing unnecessary columns
    df = df.drop(['birth_number', 'year', 'month', 'day', 'mix'], axis=1)
    
    return df 

def preProcessDisp(disp_df):
    df = disp_df.copy()
    
    df = df.rename(columns={'type': 'disp_type'})
    
    return df

def preProcessCard(card_df):
    df = card_df.copy()
    
    df['issued'] = pd.to_datetime(df['issued'], format='%y%m%d')
    df['month'] = df['issued'].dt.month
    df['year'] = df['issued'].dt.year
    df = df.drop(['card_id', 'issued'], axis=1)
    df = df.rename(columns={'type': 'card_type'})
    

    return df

def preProcessDistrict(district_df):
    df = district_df.copy()
    
    # '?' Values to average: 'no. of commited crimes \'95 '
    crimes_NOTNULL = df['no. of commited crimes \'95 '] != '?'
    crimes_NULL = df['no. of commited crimes \'95 '] == '?'
    crimes_average = pd.to_numeric(df[crimes_NOTNULL]['no. of commited crimes \'95 ']).astype(float).median()
    df.loc[crimes_NULL, 'no. of commited crimes \'95 '] = crimes_average
    
    # '?' Values to average: 'unemploymant rate \'95 '
    unemploymant_NOTNULL = df['unemploymant rate \'95 '] != '?'
    unemploymant_NULL = df['unemploymant rate \'95 '] == '?'
    unemploymant_average = pd.to_numeric(df[unemploymant_NOTNULL]['unemploymant rate \'95 ']).astype(float).median()
    df.loc[unemploymant_NULL, 'unemploymant rate \'95 '] = unemploymant_average
    
    # Int -> Float, Obj -> Numeric
    df['unemploymant rate \'95 '] = df['unemploymant rate \'95 '].astype(float)
    df['no. of commited crimes \'95 '] = pd.to_numeric(df['no. of commited crimes \'95 '])
    df['unemploymant rate \'96 '] = df['unemploymant rate \'96 '].astype(float)
    df['no. of commited crimes \'96 '] = pd.to_numeric(df['no. of commited crimes \'96 '])
    df['no. of enterpreneurs per 1000 inhabitants '] = pd.to_numeric(df['no. of enterpreneurs per 1000 inhabitants '])
    df['ratio of urban inhabitants '] = df['ratio of urban inhabitants '].astype(float)
    
    # Ratio: 0-1
    df['entrepeneurs ratio'] = df['no. of enterpreneurs per 1000 inhabitants '] / 1000
    df['ratio of urban inhabitants '] = df['ratio of urban inhabitants '] / 100
    
    # 95-96 Increase on Crimes and Unemploymant
    df['crimes_increase'] = (df['no. of commited crimes \'96 '] - df['no. of commited crimes \'95 ']) / df['no. of inhabitants']
    df['unemploymant_increase'] = df['unemploymant rate \'96 '] - df['unemploymant rate \'95 ']

    # Removing unnecessary columns
    df = df.drop(['no. of enterpreneurs per 1000 inhabitants ', 
                 'unemploymant rate \'96 ', 'no. of commited crimes \'96 ',
                  'unemploymant rate \'95 ', 'no. of commited crimes \'95 ', 'name ', 'region'], axis=1)        
    
    df = df.rename(columns={'code ': 'district_id'})

    return df

preProcessedClient_df = preProcessClient(client_df)
preProcessedDisp_df = preProcessDisp(disp_df)
preProcessedCard_df = preProcessCard(card_df)
preProcessedDistrict_df = preProcessDistrict(district_df)

def ProcessRightSide(client, disp, card, district):
    client_df = client.copy()
    disp_df = disp.copy()
    card_df = card.copy()
    district_df = district.copy()

    # Clients and Districts don't mix with anything else, so let's merge them
    client_district_df = client_df.merge(district_df, on='district_id', how='left')

    # Merging Disp and Card so we can eliminate disp_id when group by account
    disp_card_df = disp_df.merge(card_df, on='disp_id', how='left')
    disp_card_df = disp_card_df.drop(['disp_id'], axis=1)

    rightSide = disp_card_df.pivot(index='account_id', columns=['disp_type']).droplevel([0], axis=1).set_axis(['disponent_id', 'owner_id', 'disponent_card_type', 'owner_card_type', 'disponent_issued_card_month', 'owner_issued_card_month', 'disponent_issued_card_year', 'owner_issued_card_year'], axis=1).reset_index()

    rightSide = rightSide.merge(client_district_df, left_on='owner_id', right_on='client_id', how='left')
    rightSide = rightSide.merge(client_district_df, left_on='disponent_id', right_on='client_id', how='left', suffixes=('', '_disp'))

    rightSide = rightSide.drop(['client_id', 'client_id_disp', 'district_id', 'district_id_disp', 'disponent_card_type', 'disponent_issued_card_month', 'disponent_issued_card_year'], axis=1)
    rightSide = rightSide.rename(columns={'gender': 'owner_gender', 'birth': 'owner_birth', 'no. of inhabitants': 'owner_num_inhabitants',
        'no. of municipalities with inhabitants < 499 ': 'owner_num_municipalities_less_499',
        'no. of municipalities with inhabitants 500-1999': 'owner_num_municipalities_between_500_1999',
        'no. of municipalities with inhabitants 2000-9999 ': 'owner_num_municipalities_between_2000_9999',
        'no. of municipalities with inhabitants >10000 ': 'owner_num_municipalities_more_10000',
        'no. of cities ': 'owner_num_cities', 'ratio of urban inhabitants ': 'owner_inhabitants_ratio',
        'average salary ': 'owner_average_salary', 'entrepeneurs ratio': 'owner_entrepeneurs_ratio',
        'crimes_increase': 'owner_crimes_increase', 'unemploymant_increase': 'owner_unemploymant_increase'})
    rightSide = rightSide.rename(columns={'gender_disp': 'disponent_gender', 'birth_disp': 'disponent_birth', 'no. of inhabitants_disp': 'disponent_num_inhabitants',
        'no. of municipalities with inhabitants < 499 _disp': 'disponent_num_municipalities_less_499',
        'no. of municipalities with inhabitants 500-1999_disp': 'disponent_num_municipalities_between_500_1999',
        'no. of municipalities with inhabitants 2000-9999 _disp': 'disponent_num_municipalities_between_2000_9999',
        'no. of municipalities with inhabitants >10000 _disp': 'disponent_num_municipalities_more_10000',
        'no. of cities _disp': 'disponent_num_cities', 'ratio of urban inhabitants _disp': 'disponent_inhabitants_ratio',
        'average salary _disp': 'disponent_average_salary', 'entrepeneurs ratio_disp': 'disponent_entrepeneurs_ratio',
        'crimes_increase_disp': 'disponent_crimes_increase', 'unemploymant_increase_disp': 'disponent_unemploymant_increase'})
    
    return rightSide
    
rightSide = ProcessRightSide(preProcessedClient_df, preProcessedDisp_df, preProcessedCard_df, preProcessedDistrict_df)
print(rightSide)
print(rightSide.isnull().sum())