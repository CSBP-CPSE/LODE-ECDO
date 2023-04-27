import pandas as pd
import os
from os import listdir
from pathlib import Path
import numpy as np
import string
import glob


# Concatenate all files 
df = pd.concat([pd.read_csv(file) for file in glob.glob('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/*.csv')])

# Removed "idx" (because redundant) and 'active' (because only one dataset had this info, and would be hard to keep updated).
df = df[['filename', 'facility_name', 'facility_type', 'health_authority', 'alternative_name', 'number_beds',
'address_str', 'street_no', 'street_name', 'street_addr', 'city', 'province', 'postal_code', 'provider', 
'latitude', 'longitude', 'phone', 'email', 'website' ]]


# Make postal codes consistent and put spaces instead of '_' + capitalize
df['postal_code'] = df['postal_code'].str.replace(' ','').str.upper()
df['facility_type'] = df['facility_type'].str.replace('_',' ')
# The code below is to convert the columns to integers. I've only needed to use it once and subsequent tries spit out an error. 
# But if you find these columns become floats again, uncomment and run once 
df['number_beds'] = df['number_beds'].round(0).astype(pd.Int64Dtype())
df['street_no'] = df['street_no'].round(0).astype(pd.Int64Dtype())


# Standardize facility_type
labkeywords = 'laboratory'
pharkeywords = 'pharmacy|pharmacies'
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
mentkeywords = 'mental|psychiatric|rehabilitation'
urgkeywords = 'urgent|emergency'
ltckeywords = 'residence|residential|résidence|nursing|palliative|senior|special care|seinor|long term|hospice|C.H.S.L.D.|specialized care|long care|long-term|assisted|nursing|retirement|personal care|chronic'
ambkeywords = 'community|clinic|walk in|primary care|tertiary|C.L.S.C.|regional|health centre|family|basic|ambulatory|autres|health network|other|primary|independent|public health|children|acquired injury|AIDS'
covidkeywords = 'covid|immunization|vaccine'

df.loc[df['facility_type'].str.contains(labkeywords, case=False, na=False), 'facility_type'] = 'Laboratory'
df.loc[df['facility_type'].str.contains(pharkeywords, case=False, na=False), 'facility_type'] = 'Pharmacy'
df.loc[df['facility_type'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'
df.loc[df['facility_type'].str.contains(mentkeywords, case=False, na=False), 'facility_type'] = 'Mental health and rehabilitation facilities'
df.loc[df['facility_type'].str.contains(urgkeywords, case=False, na=False), 'facility_type'] = 'Urgent care facilities'
df.loc[df['facility_type'].str.contains(ltckeywords, case=False, na=False), 'facility_type'] = 'Nursing and residential care facilities'
df.loc[df['facility_type'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_type'].str.contains(covidkeywords, case=False, na=False), 'facility_type'] = 'Covid-19 related facilities'

# Add column to show if geosourcing is necessary
df.loc[~df.latitude.isnull(), 'geo_source']='Source'

df = df.reset_index(drop=True)
df.to_csv('merged.csv')
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/4-Parsing/merged.csv')


