# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:00:13 2020

@author: joseph
"""

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import jellyfish


dupes=pd.read_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\CURRENT\healthfacilitiesproject-2020-04-05\workspace\03-detected_dupes.csv",
                  dtype=str)

reals=[]
lev=[]
partial_lev=[]
jaro_winkler=[]
dupes=dupes.dropna(subset=['hospital_name','name_f'])
dupes=dupes.fillna('')
name1=list(dupes.hospital_name)
name2=list(dupes.name_f)

for i in range(len(name1)):
    
    rat=fuzz.ratio(name1[i],name2[i])
    rat2=fuzz.partial_token_sort_ratio(name1[i],name2[i])
    JW=jellyfish.jaro_winkler(name1[i], name2[i])*100
    lev.append(rat)
    partial_lev.append(rat2)
    jaro_winkler.append(JW)
    if (rat>=75 or rat2>=85 ):
        reals.append(True)
    
    else:
        reals.append('')
        
dupes['levenshtein']=lev
dupes['PartialLevenshtein']=partial_lev

dupes['RealDupe']=reals

#read in full file to add in NAICS info when possible

df=pd.read_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\CURRENT\healthfacilitiesproject-2020-04-05\workspace\04-dataset_ManualProcessing.csv",
               encoding='cp1252',dtype=str)

list(df)
df=df[['index','provider','NAICS_code']]

dupes=pd.merge(dupes,df,how='left',on='index')
dupes=pd.merge(dupes,df,how='left',left_on='index_f',right_on='index',suffixes=('','_2'))
dupes=dupes[['index',
 'hospital_name',
 'province',
 'longitude',
 'latitude',
 'street_no',
 'street_name',
  'provider',
 'NAICS_code',
 'dist',
 'prov_eq',
 'score',
 'index_f',
 'name_f',
 'longitude_f',
 'latitude_f',
 'street_no_f',
 'street_name_f',
 'provider_2',
 'NAICS_code_2',
  'levenshtein',
 'PartialLevenshtein',
 'RealDupe'
]]

dupes=dupes.loc[dupes.RealDupe==True]
dupes['NAICS_Sim']=dupes['NAICS_code']==dupes['NAICS_code_2']

dupes=dupes.loc[dupes.NAICS_Sim==True]

dupes.to_csv('dupes_naics.csv',index=False)