"""This script compares names of facilities returned by Nominatim to the originals, and keeps them if they are good matches"""

import pandas as pd
from fuzzywuzzy import fuzz
df = pd.read_csv("ODEFv2_Geocoded_AGOL_OSM_29-03-2021.csv", dtype="str",low_memory=False)

score=[]
name1=list(df['facility_name'].str.upper())
name2=list(df['osm_name'].fillna('').str.upper())

for i in range(len(df)):
    n1=name1[i]
    n2=name2[i]
    if n2!='':
        score.append(fuzz.partial_ratio(n1,n2))
    else:
        score.append(0)
df['fuzzy_score']=score

df['keep']=''

print(df.osm_type.unique())
types=['school', 'prison', 'university', 'college',
     'community_centre',  'social_facility', 'kindergarten', 'townhall']
df.loc[(df.fuzzy_score>=90) & df['osm_type'].isin(types),'keep']=True

df.loc[df.keep==True,'latitude'] = df.osm_lat
df.loc[df.keep==True,'longitude'] = df.osm_lon
df.loc[df.keep==True,'geo_source'] = 'Nominatim'

df.to_csv('ODEF_Geocoded_Valid.csv',index=False)