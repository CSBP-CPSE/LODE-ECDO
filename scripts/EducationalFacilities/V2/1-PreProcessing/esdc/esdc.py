"""
this script does some preprocessing on the list of designated institutions received from ESDC 
In particular, addresses are broken into 3 fields, with empty values populated with NULL,
opentabulate can't deal with this itself, so this script removes the NULL values """

import pandas as pd

df=pd.read_csv('CSLPPD_Data_MDL.csv', na_values='null')
df.to_csv('ESDC_Designated_Institutions.csv',index=False,encoding='utf-8')