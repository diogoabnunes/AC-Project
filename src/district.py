import pandas as pd

district_fields = [
                    'code ',
                    'name ',
                    'region',
                    'no. of inhabitants',
                    'no. of municipalities with inhabitants < 499 ',
                    'no. of municipalities with inhabitants 500-1999',
                    'no. of municipalities with inhabitants 2000-9999 ',
                    'no. of municipalities with inhabitants >10000 ',
                    'no. of cities ',
                    'ratio of urban inhabitants ',
                    'average salary ',
                    'unemploymant rate \'95 ',
                    'unemploymant rate \'96 ',
                    'no. of enterpreneurs per 1000 inhabitants ',
                    'no. of commited crimes \'95 ',
                    'no. of commited crimes \'96 '
                ]

district = pd.read_csv('../data/district.csv', usecols=district_fields, sep=';', na_values='?')

unique_districts = district['code '].nunique()
unique_regions = district['region'].nunique()
urban_inhabitants = district['no. of inhabitants'].multiply(district['ratio of urban inhabitants '])
salary_correlation = urban_inhabitants.corr(district['average salary '])
inhabitants = {}

for i, d in district.iterrows():
    if d['region'] not in inhabitants:
        inhabitants[d['region']] = d['no. of inhabitants']
    else:
        inhabitants[d['region']] += d['no. of inhabitants']

print(f'No. of districts: {unique_districts}')
print(f'No. of regions: {unique_regions}')
print('No. of inhabitants per region:')
for key in inhabitants:
    print(f'    - {key}: {inhabitants[key]}')
print(f'Correlation between urban inhabitants and average salary in the districts: {salary_correlation}')

client_fields = ['client_id', 'birth_number', 'district_id', 'gender']
client = pd.read_csv('../data/updatedClient.csv', usecols=client_fields, sep=',')

clients_district = client['district_id'].value_counts()
# Of all the 77 districts, only 6 have at least 100 clients
print(f'Clients per district:\n{clients_district}')
