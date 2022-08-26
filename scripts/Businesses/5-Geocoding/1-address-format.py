# copied 08-25 - not the most up to date version

# this script is to applies formating to addresses

# The formatting functions apply three main processes to the input addresses. These are
# * removing punctuation
# * standardising directions (e.g., north &rarr; n)
# * standardising street types (e.g., street &rarr; st)

import pandas as pd
from Address_Format_Funcs import AddressClean_en, AddressClean_fr

df = pd.read_csv('data/4-ODBiz_merged_2022-08-04.csv')

# FOR TESTING we are removing any records which have no street number or name
# and restricting the columns

# let's stop doing that. do this at the address matching stage

# df = df[df['street_name'].notna()]
# df = df[df['street_no'].notna()]
df = df[['localfile', 'province', 'city', 'mailing_address', 'street_no', 'street_name', 'latitude', 'longitude']]
# sample = df.sample(100)

# apply formatting functions
# test = df
df = AddressClean_en(df,'street_name','formatted_en')
# df = AddressClean_fr(df,'street_name','formatted_fr')

df = AddressClean_fr(df,'street_name','formatted_fr')

df.to_csv('formatted_25.csv',index=False)