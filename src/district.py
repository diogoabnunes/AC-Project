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
inhabitants = {}
for i, d in district.iterrows():
    if d['region'] not in inhabitants:
        inhabitants[d['region']] = d['no. of inhabitants']
    else:
        inhabitants[d['region']] += d['no. of inhabitants']
avg_salary = {}
for i, d in district.iterrows():
    

print(f'No. of districts: {unique_districts}')
print(f'No. of regions: {unique_regions}')
print('No. of inhabitants per region:')
for key in inhabitants:
    print(f'    - {key}: {inhabitants[key]}')