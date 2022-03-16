# -*- coding: utf-8 -*-
"""
This script looks for potential duplicates in a database
in this case, we're considering health facilities

we block on Province, so only entries in the same province are compared
and we then compare facility name, address, and city information
We will also consider distance between entries, when possible
"""

import pandas as pd
import recordlinkage as rl
from recordlinkage.preprocessing import clean
from recordlinkage.base import BaseCompareFeature
from numpy import arcsin, sin, cos, sqrt,radians

class CompareCoords(BaseCompareFeature):

    def _compute_vectorized(self, lat1, lon1, lat2, lon2):
        """Compare coordinates using haversine distance.

        """
        lat1=radians(lat1)
        lon1=radians(lon1)
        lat2=radians(lat2)
        lon2=radians(lon2)

        re=6371E3 #Earth radius
        temp1=sin((lat2-lat1)/2.)*2
        temp2=cos(lat1)*cos(lat2)*sin((lon2-lon1)/2.)**2
        d=2*re*arcsin(sqrt(temp1+temp2))
        return d


#read in database - this assumes it's in utf-8 encoding
#standard windows (excel) encoding is cp1252
df=pd.read_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\healthfacilitiesproject-2020-03-19\02-0-dataset.csv")#encoding='cp1252'

"""
This section should not be permanent, but right now there are facilities (mainly MB)
that have not been assigned a Province
"""

df.loc[(df['province'].isnull())&(df.provider=='Province of Manitoba'),'province']='MB'

#we'll be doing some cleaning to make matching easier, like dropping accents,
#but we still want them in the database, so we'll make a copy of the database 
#for the linkage process


DF=df.copy()
DF['latitude']=df.latitude.str.rstrip(',')
DF['latitude']=DF['latitude'].astype(float)
DF['longitude']=DF['longitude'].astype(float)

DF['hospital_name']=clean(DF['hospital_name'])
DF['street_name']=clean(DF['street_name'])
DF['city']=clean(DF['city'])
DF['address_str']=clean(DF['address_str'])

#compute candidate pairs for record comparison

indexer = rl.Index()
indexer.block('province')
candidate_links = indexer.index(DF)

# Comparison step
compare = rl.Compare()

compare.exact('street_no', 'street_no', label='streetnum_match')
compare.string('address_str', 'address_str', method='jarowinkler',  label='fulladdr_match')
compare.string('street_name', 'street_name', method='jarowinkler',  label='street_match')
compare.string('city', 'city',  label='city_match')
compare.string('hospital_name', 'hospital_name',  label='name_match')

compare.add(CompareCoords(('latitude','longitude'),('latitude','longitude'),label='proximity_match'))

features = compare.compute(candidate_links, DF)

features=features.loc[(features.proximity_match.isnull())|(features.proximity_match<2E3)]

"""
define criteria for potential duplicates:
    
    1. within 1km of each other
    2. Same city (city score>0.9), and similar full addr
    3 Same city, same street num, similar street name
    4. Same city, same facility name
"""

f=features.loc[(features.proximity_match<1E3)|((features.city_match>0.8)&(features.fulladdr_match>0.8))|((features.city_match>0.8)&(features.streetnum_match==1)&(features.street_match>0.8))|((features.city_match>0.8)&(features.name_match>0.8))]
f=f.reset_index()

idx1=list(f.level_0)
idx2=list(f.level_1)
NAME1=[]
NAME2=[]
NUM1=[]
NUM2=[]
STREET1=[]
STREET2=[]
CITY1=[]
CITY2=[]
LAT1=[]
LAT2=[]
LON1=[]
LON2=[]
for i in range(len(idx1)):
    
    NAME1.append(DF.loc[idx1[i],'hospital_name'])
    NAME2.append(DF.loc[idx2[i],'hospital_name'])
    NUM1.append(DF.loc[idx1[i],'street_no'])
    NUM2.append(DF.loc[idx2[i],'street_no'])
    STREET1.append(DF.loc[idx1[i],'street_name'])
    STREET2.append(DF.loc[idx2[i],'street_name'])
    CITY1.append(DF.loc[idx1[i],'city'])
    CITY2.append(DF.loc[idx2[i],'city'])
    LAT1.append(DF.loc[idx1[i],'latitude'])
    LAT2.append(DF.loc[idx2[i],'latitude'])
    LON1.append(DF.loc[idx1[i],'longitude'])
    LON2.append(DF.loc[idx2[i],'longitude'])
f['NAME1']=NAME1
f['NAME2']=NAME2
f['NUM1']=NUM1
f['NUM2']=NUM2
f['STREET1']=STREET1
f['STREET2']=STREET2
f['CITY1']=CITY1
f['CITY2']=CITY2
f['LAT1']=LAT1
f['LAT2']=LAT2
f['LON1']=LON1
f['LON2']=LON2
f=f.sort_values(by=['level_0'],ascending=True)
f.to_csv('test.csv',index=False,encoding='cp1252')