import pandas as pd
import os
from os import listdir
from hashlib import blake2b
from pathlib import Path
import numpy as np
import string


# Concatenate all files
pdir = "/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output"
files = listdir(pdir)
DFS = []

for file in files:
    filepath = os.path.join(pdir, file)
    df_temp = pd.read_csv(filepath)
    DFS.append(df_temp)

df = pd.concat(DFS)


# Removed "idx" (because redundant) and 'active' (because only one dataset had this info, and would be hard to keep updated). 
# **** DON'T FORGET TO ADD PROVINCE LATER ****
df = df[['facility_name', 'facility_type', 'health_authority', 'alternative_name', 'number_beds',
'address_str', 'street_no', 'street_name', 'street_addr', 'city', 'province', 'postal_code', 'provider', 
'latitude', 'longitude', 'phone', 'email', 'website' ]]


# Make postal codes consistent and put spaces instead of '_' + capitalize
df['postal_code'] = df['postal_code'].str.replace(' ','').str.upper()
df['facility_type'] = df['facility_type'].str.replace('_',' ')


# Standardize facility_type
pharkeywords = 'pharmacy|pharmacies'
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ltckeywords = 'residence|residential|résidence|nursing|palliative|senior|special care|seinor|long term|hospice'
ambkeywords = 'community|clinic|walk in|primary care|tertiary'
covidkeywords = 'covid|immunization|vaccine'

df.loc[df['facility_type'].str.contains(pharkeywords, case=False, na=False), 'facility_type'] = 'TYPE 0'
df.loc[df['facility_type'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'TYPE 1'
df.loc[df['facility_type'].str.contains(ltckeywords, case=False, na=False), 'facility_type'] = 'TYPE 2'
df.loc[df['facility_type'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'TYPE 3'
df.loc[df['facility_type'].str.contains(covidkeywords, case=False, na=False), 'facility_type'] = 'TYPE 4'


df = df.reset_index(drop=True)
df.to_csv('merged.csv')
print(df['facility_type'].unique())
print(df.duplicated(subset=['street_addr']))
df.dtypes