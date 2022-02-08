"""
Concatenate all opentab output into one file, and add unique identifier.
"""

import pandas as pd
from os import listdir
from hashlib import blake2b

def GetHash(x):
    
    h=blake2b(digest_size=10)
    h.update(x.encode())
    return h.hexdigest()
            
            


#read in all parsed files and concatenate together
pdir="/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output"

sources=['ab','bc','mb','nb','nl','ns','nt','nu','on','pe','qc','sk','yt']
DFS=[]
for s in sources:
    files=[f for f in listdir("{}/{}".format(pdir,s)) if f.endswith('.csv')]
    for f in files:
        df_temp=pd.read_csv("{}/{}/{}".format(pdir,s,f),dtype=str, low_memory=False)
        DFS.append(df_temp)

df=pd.concat(DFS)

#restrict to only desired columns

#columns to be assessed after opentab run: idx, source_id, geo_source
df=df[['idx', 'source_id', 'facility_name', 'facility_type', 'operator_name', 'health_authority', 'alternative_name', 'number_beds', 'active', 'address_str', 'street_no', 'street_name', 'street_addr', 'city', 'province', 'postal_code', 'provider', 'latitude', 'longitude','geo_source', 'phone', 'email', 'website' ]]



#standardise province names

df.loc[df.provider=='Province of Alberta','province']='AB'
df.loc[df.provider=='Province of British Columbia','province']='BC'
df.loc[df.provider=='Province of Ontario','province']='ON'
df.loc[df.provider=='Province of Québec','province']='QC'
df.loc[df.provider=='Province of Saskatchewan','province']='SK'
df.loc[df.provider=='Province of Nova Scotia','province']='NS'

provs_dict={'Alberta':'AB',
           'British Columbia':'BC',
           'Manitoba':'MB',
           'New Brunswick':'NB',
           'Newfoundland and Labrador':'NL',
           'Nova Scotia':'NS',
            'Northwest Territories':'NT',
            'Nunavut':'NU',
           'Ontario':'ON',
           'Prince Edward Island':'PE',
           'Quebec':'QC',
           'Saskatchewan':'SK',
           'Yukon Territories':'YT',
           'Yukon':'YT'}


for key in provs_dict:
    df['province'] = df['province'].str.replace(key, provs_dict[key],regex=False)
    

#make postal codes consistent

df['postal_code']=df['postal_code'].str.replace(' ','').str.upper()


"""
Code below to be modified to fit ODHF needs, examples from ODEF remain.
Thoughts:
- dropping facilities that do not fit into our categories such as eye exam locations and dentists
- since York hospital file only one with variable 'active', maybe just remove records that show status is non-active then drop variable
- 
"""


#Drop entries that shouldn't be included

drop_list=['Home-based School']

for d in drop_list:
    df.drop(df.loc[df['facility_name']==d].index, inplace=True)
    
    
    
# SL - we will also probabably want to standardize health facility types
# I believe there is a link somewhere
    

#finally, replace index with fresh index

df['idx_basic']=range(1,1+len(df))

#Use temporary column and hash function to create new identifier

def make_temp_col(df):
    df_temp=df.copy()
    cols=['source_id','facility_name','address_str','provider']
    del_list=[" ","-","'","."]
    for col in cols:
    
        df_temp[col]=df_temp[col].str.upper()
        df_temp[col]=df_temp[col].fillna('NULL')
    
        for i in del_list:
            df_temp[col]=df_temp[col].str.replace(i,'',regex=False)
    df_temp['temp']=df_temp['source_id']+'-'+df_temp['facility_name']+'-'+df_temp['address_str']+'-'+df_temp['provider']
    return df_temp['temp']

df['temp']=make_temp_col(df)
df['idx']=df['temp'].apply(GetHash)

#fill in geo_method

df.loc[~df.latitude.isnull(), 'geo_source']='Source'

print(len(df), 'entries in database')


df.to_csv('ODHFv2_concat.csv',index=False)
