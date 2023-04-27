"""
When fixes are applied earlier in the chain, we don't want to have to re-do geocoding.
This file takes the latest version of the ODEF from the parsing step, and joins it on "ODEF_Geocoded_Valid"
"""
import pandas as pd

df=pd.read_csv("../4-Parsing/ODEFv2_31-03-2021_parsed.csv", dtype="str", low_memory=False)

df_geo = pd.read_csv("ODEF_Geocoded_Valid.csv", dtype="str", low_memory=False)


#merging doesn't work well with duplicates, so we'll do a simple deduplication here

df_geo['dupe']=df_geo.duplicated(subset=['provider','source_id', 'facility_name','address_str','city','ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+'], keep=False)
df['dupe']=df.duplicated(subset=['provider','source_id', 'facility_name','address_str','city','ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+'], keep=False)

df.loc[df.dupe==True].to_csv('simple_duplicates_check.csv',index=False)
df_geo.loc[df_geo.dupe==True].to_csv('simple_duplicates_geo_check.csv',index=False)

df_geo=df_geo.drop_duplicates(subset=['provider','source_id', 'facility_name','address_str','city','ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+'])
df=df.drop_duplicates(subset=['provider','source_id', 'facility_name','address_str','city','ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+'])

print(len(df_geo)-len(df))

#we will do it in two steps. First on records with source_ids, and then on those that don't.

df_source=df.copy()
df_none=df.copy()

df_source=df_source.loc[~df_source.source_id.isnull()]
df_none=df_none.loc[df_none.source_id.isnull()]

df1 = pd.merge(df_source, df_geo, on=['source_id', 'provider'], how='left', suffixes=('','_y'))
df2 = pd.merge(df_none, df_geo, on=['facility_name', 'provider','city','address_str'], how='left', suffixes=('','_y'))



print(len(df), len(df1)+len(df2))

DF=pd.concat([df1,df2])

DF['latitude']=DF['latitude_y']
DF['longitude']=DF['longitude_y']
DF['geo_source']=DF['geo_source_y']

#drop all duplicate columns

full_list=list(DF)
drop_list=[x for x in full_list if x.endswith('_y')]

DF=DF.drop(columns=drop_list)

DF.to_csv("output/ODEFv2_Geocoded_31-03-2021.csv",index=False)