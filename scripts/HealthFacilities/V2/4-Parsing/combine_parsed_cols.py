import pandas as pd
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)


f_in = "parsed.csv"
f_out = "combined.csv"
df=pd.read_csv(f_in, low_memory=False, dtype='str')


df['unit'] = np.nan

# Merge parsed columns with other columns
df['street_no'] = df['street_no'].fillna(df['LP2_street_no'])
df['street_name'] = df['street_name'].fillna(df['LP_street_name'])
df['postal_code'] = df['postal_code'].fillna(df['LP_PostCode'].str.upper())
df['city'] = df['city'].fillna(df['LP_City'].str.capitalize())
df['unit'] = df["LP3_unit"].str.capitalize()

# Reorder columns
df = df[['facility_name', 'facility_type', 'health_authority', 'alternative_name', 'number_beds',
'address_str', 'unit', 'street_no', 'street_name', 'street_addr', 'city', 'province', 'postal_code', 'provider', 
'latitude', 'longitude', 'phone', 'email', 'website' ]]

# Remove all postal codes that are not 6 characters long and that do not follow the format of a postal code
df['postal_code'] = df['postal_code'].str.replace(' ','').str.upper()
df['postal_code'] = df['postal_code'].str.replace('-','').str.upper()
df = df[df['postal_code'].str.len()==6]

first = df['postal_code'].astype(str).str[0]
second = df['postal_code'].astype(str).str[1]
third = df['postal_code'].astype(str).str[2]
fourth = df['postal_code'].astype(str).str[3]
fifth = df['postal_code'].astype(str).str[4]
sixth = df['postal_code'].astype(str).str[5]
df['postal_code'][first.str.isdigit()] = ''
df['postal_code'][second.str.isalpha()] = ''
df['postal_code'][third.str.isdigit()] = ''
df['postal_code'][fourth.str.isalpha()] = ''
df['postal_code'][fifth.str.isdigit()] = ''
df['postal_code'][sixth.str.isalpha()] = ''










print(df['postal_code'].unique())







#units = df['street_no'].str.contains(' ', na=False)
#print(units)
#print(np.where(units)[0])







f_out = df.to_csv(f_out, index=False)






