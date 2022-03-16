import pandas as pd
import numpy as np
import sys
from hashlib import blake2b
#np.set_printoptions(threshold=sys.maxsize)


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
df = df[['filename', 'facility_name', 'facility_type', 'health_authority', 'alternative_name', 'number_beds',
'address_str', 'unit', 'street_no', 'street_name', 'street_addr', 'city', 'province', 'postal_code', 'provider', 
'latitude', 'longitude', 'geo_source', 'phone', 'email', 'website' ]]

# Remove all postal codes that are not 6 characters long and that do not follow the format of a postal code
df['postal_code'] = df['postal_code'].str.replace(' ','').str.upper()
df['postal_code'] = df['postal_code'].str.replace('-','').str.upper()
mask = df['postal_code'].astype(str).str.len() != 6
df.loc[mask, 'postal_code'] = ''
#print(df['postal_code'].tolist())


#Create unique identifiers for each datapoint
def GetHash(x):
    h=blake2b(digest_size=15)
    h.update(x.encode())
    return h.hexdigest()

def make_temp_col(df):
    df_temp=df.copy()
    cols=['facility_name','street_name','city','latitude','street_no','longitude','facility_type']
    del_list=["-","'","."]
    for col in cols:
    
        df_temp[col]=df_temp[col].str.upper()
        df_temp[col]=df_temp[col].fillna('NULL')
    
        for i in del_list:
            df_temp[col]=df_temp[col].str.replace(i,'',regex=False)
    df_temp['temp']=df_temp['facility_name']+'-'+df_temp['street_name']+'-'+df_temp['city']+'-'+df_temp['latitude']+'-'+df_temp['street_no']+'-'+df_temp['longitude']+'-'+df_temp['facility_type']
    return df_temp['temp']

df['temp']=make_temp_col(df)
df['idx']=df['temp'].apply(GetHash)

#Any indexes that are the same basically mean that the data points are the same, which is why we drop duplicates
df = df.drop_duplicates(subset=['idx'])
df = df.drop(['temp'], axis=1)
df.insert(0, 'idx', df.pop('idx'))

df.to_csv(f_out, index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/5-Geocoding/combined.csv', index=False)
print(df['idx'].value_counts())





