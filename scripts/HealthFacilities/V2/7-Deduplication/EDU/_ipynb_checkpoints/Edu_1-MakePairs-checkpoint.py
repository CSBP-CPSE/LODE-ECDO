# -*- coding: utf-8 -*-
r"""
This script looks for potential duplicates in a database

We are assuming a set of standard columns,
Name, Address, StreetNumber, StreetName, City, PostalCode, Province, Latitude, Longitude

There are two sections, an initial Preprocessing step, and then the comparison script

With minor modification, this can also be used for record linkage between two files.

I) Preprocessing:
    0. Read in JSON 'source' file that contains
        i. file name of database
        ii. mappings from database column names to standard names
        iii. a short dictionary of terms to replace in the Name field to improve
            potential matches (e.g., 'ch' for 'centre hospitalier')
    1. Read in database (columns as values from json)
    2. Strip all accents from all text fields
    3. Process Address and Street Name fields to standardise street types
    4. run recordlinkage's "clean" function to remove extra whitespace and any
        remaining non-ascii characters, and anything in parentheses
    5. Standardise PostalCode
        
II) Record Linkage:
    Use RecordLinkageToolkit to perform comparisons and create index pairs:
        Criteria:
                CSDUID - Block (consider only matches where equal)
                Name - Damerau-Levenshtein, qgram
                Address - Damerau-Levenshtein, Cosine
                StreetNumber - Exact
                StreetName - Damerau-Levenshtein, Cosine
                City - Damerau-Levenshtein
                PostalCode - Exact
                Latitude/Longitude - Distance
                


    The result is a Pandas multiindex object, which we then use to create a file
    where every line contains the two objects being compared. 
    
    
    
    This output file can be fed to a machine learning script for classification.
"""
import json
import pandas as pd
import re
from rl_helper import strip_accents, AddressClean, haversine
import recordlinkage as rl
from recordlinkage.preprocessing import clean
from recordlinkage.index import Block
import numpy as np
import math

r'''
Read in source file, data file, and rename data file columns
'''
sourcefile=r"input/ODEF_Source.json"
with open(sourcefile) as source_f:
    Source=json.load(source_f)
    

DF=pd.read_csv(Source["filename"],
               encoding=Source["encoding"],
               index_col=Source["index"], low_memory=False, dtype='str')

#reduce database to only the columns we use for comparisons
DF=DF[Source["column_map"].values()]
column_map={val: key for key, val in Source["column_map"].items()}
DF=DF.rename(columns=column_map)
df=DF.copy()


"""
We want to block on ISCED so that schools are only considered duplicates if their grade ranges are the same.
We'll fill empty values with 0 in case nulls make it difficult for the matching
"""
cols=['ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+']


    
for c in cols:
    df[c]=df[c].fillna('0')
    


df['ISCED_SUM']=df['ISCED020'].astype(int) + df['ISCED1'].astype(int) + df['ISCED2'].astype(int) + df['ISCED3'].astype(int) + df['ISCED4+'].astype(int)
df=df.sort_values(by=['CSDUID','Name','ISCED_SUM'],ascending=False)


print('I. Preprocessing - renaming columns, removing accents, and making string replacements.')

#remove accents

text_cols=['Name','Address','StreetName','City']
for col in text_cols:
    
    df.loc[~df[col].isnull(),col]=df.loc[~df[col].isnull(),col].apply(strip_accents)
    
#apply text swaps in the Name column    
for swap in Source["text_map"]:
    start=r'\b'+re.escape(swap[0])+r'\b'
    df["Name"]=df["Name"].str.replace(start,swap[1], regex=True)
    



#standardise addresses 

df.loc[(~df['StreetName'].isnull())&(df.Province!='QC'),'StreetName']=df.loc[(~df['StreetName'].isnull())&(df.Province!='QC'),'StreetName'].apply(AddressClean, args=('en',))
df.loc[(~df['StreetName'].isnull())&(df.Province=='QC'),'StreetName']=df.loc[(~df['StreetName'].isnull())&(df.Province=='QC'),'StreetName'].apply(AddressClean, args=('fr',))

df.loc[(~df['Address'].isnull())&(df.Province!='QC'),'Address']=df.loc[(~df['Address'].isnull())&(df.Province!='QC'),'Address'].apply(AddressClean, args=('en',))
df.loc[(~df['Address'].isnull())&(df.Province=='QC'),'Address']=df.loc[(~df['Address'].isnull())&(df.Province=='QC'),'Address'].apply(AddressClean, args=('fr',))

#remove periods, apostrophes, commas, and hypens in the Name and address columns

r_list=[r".",r",",r"'",r"-"]

for r in r_list:
    
    df["Name"]=df["Name"].str.replace(r,' ',regex=False)
    df["Address"]=df["Address"].str.replace(r,' ',regex=False)

#remove excess whitespace
df["Name"]=df["Name"].str.replace(r" +"," ",regex=True)
df["Address"]=df["Address"].str.replace(r" +"," ",regex=True)

#standardise postal codes - just remove empty space and make sure it's all lower case

df.loc[~df.PostalCode.isnull(),'PostalCode']=df.loc[~df.PostalCode.isnull(),'PostalCode'].str.replace(' ','').str.lower()

#create an extra temporary Name column with an additional level of cleaning

df['NameClean']=clean(df["Name"])

#Some records have street number and street name, but no address field filled

df.loc[(df.Address.isnull())&\
       (~df.StreetName.isnull()),'Address']\
    =clean(df.loc[(df.Address.isnull())&\
       (~df.StreetName.isnull()),'StreetNumber']+' '+\
           df.loc[(df.Address.isnull())&\
       (~df.StreetName.isnull()),'StreetName']+' '+\
        df.loc[(df.Address.isnull())&\
       (~df.StreetName.isnull()),'City'])

print('1.b) Simple Deduplication - use Pandas to drop identical rows before additional processing')

df['dupe']=df.duplicated(subset=['Name','Address','CSDUID','ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+'],keep='first')
df.loc[df.dupe==True].to_csv('output/simple_dupes.csv',encoding='utf-8')
df=df.drop_duplicates(subset=['Name','Address','CSDUID', 'ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+'],keep='last')


r"""
II. Record Linkage


This is the section that uses the record linkage package to determine candidate pairs,
which will be evaluated separately.
"""
"""
print('II. Record linkage - Now creating multiindex and performing comparisons')
indexer = rl.Index()
#indexer.block('Province')
indexer.add(Block('CSDUID'))
#indexer.add(Block('ISCED020'))
#indexer.add(Block('ISCED1'))
#indexer.add(Block('ISCED2'))
#indexer.add(Block('ISCED3'))
#indexer.add(Block('ISCED4+'))


candidate_links = indexer.index(df)

print (len(df)**2, len(candidate_links))

print('Computing metrics for {} candidate pairs'.format(len(candidate_links)))

#likely to be a lot of records to match, so split into chunks
n=math.ceil(len(candidate_links)/1E5)
chunks=rl.index_split(candidate_links, n)
# Comparison step
results=[]
#n_jobs specifies number of cores for running in parallel
compare = rl.Compare(n_jobs=8) 
    
compare.exact('StreetNumber', 'StreetNumber', label='StrNum_Match')
compare.exact('PostalCode', 'PostalCode', label='PC_Match')
compare.exact('ISCED020','ISCED020',label='ISCED020_Match')
compare.exact('ISCED1','ISCED1',label='ISCED1_Match')
compare.exact('ISCED2','ISCED2',label='ISCED2_Match')
compare.exact('ISCED3','ISCED3',label='ISCED3_Match')
compare.exact('ISCED4+','ISCED4+',label='ISCED4+_Match')

compare.string('Address', 'Address', method='cosine',  label='Addr_CS')
compare.string('Address', 'Address', method='lcs',  label='Addr_LCS')

compare.string('StreetName', 'StreetName', method='damerau_levenshtein',  label='StrName_DL')
compare.string('StreetName', 'StreetName', method='cosine',  label='StrName_CS')
    
compare.string('City', 'City',  method='damerau_levenshtein',label='City_DL')
compare.string('Name', 'Name',  method='damerau_levenshtein',label='Name_DL')
compare.string('Name', 'Name',  method='cosine',label='Name_CS')

    
compare.string("NameClean","NameClean",method='damerau_levenshtein',label="CleanName_DL")
i=0
for chunk in chunks:
    i+=1
    print('processing chunk {} of {}'.format(i,n))

    
    features = compare.compute(chunk, df)

    #reduce comparison matrix to entries where the name score is reasonably high

    cutoff=0.9
    features=features.loc[features.Name_CS>cutoff]
    results.append(features)
f=pd.concat(results)
print('Score cut-off of {} reduced candidate pairs to {}'.format(cutoff,len(f)))

f['idx1']=f.index.get_level_values(0)
f['idx2']=f.index.get_level_values(1)

print('Merging on original dataframe and computing distance.')
f=f.merge(df,left_on='idx1',how='left',right_on='idx')

f=f.merge(df,left_on='idx2',how='left',right_on='idx', suffixes=('_1','_2'))

f['Distance']=np.nan

f.loc[(~f.Latitude_1.isnull())&(~f.Latitude_2.isnull()),'Distance']=f.loc[(~f.Latitude_1.isnull())&(~f.Latitude_2.isnull())].apply(lambda row: haversine(row), axis=1)

f=f[['idx1',
     'idx2',
     'Name_1',
     'Name_2',
     'Name_DL',
     'Name_CS',
     'Addr_CS',
     'Addr_LCS',
     'Address_1',
     'Address_2',
     'StrNum_Match',
     'StrName_DL',
     'StrName_CS',
     'PC_Match',
     'Distance',
    'ISCED020_Match',
    'ISCED1_Match',
    'ISCED2_Match',
    'ISCED3_Match',
    'ISCED4+_Match']]

f.to_csv('{}'.format(Source["output_name"]),index=False,encoding='cp1252')
#f.loc[(~f.Distance.isnull())&\
#     (~f.Address_1.isnull())&\
#          (~f.Address_2.isnull())].\
#    to_csv('{}_FullInfo.csv'.format(Source["output_name"]),index=False,encoding='cp1252')

#f.loc[(f.Distance.isnull())|\
#      (f.Address_1.isnull())|\
#          (f.Address_2.isnull())].\
#    to_csv('{}_PartialInfo.csv'.format(Source["output_name"]),index=False,encoding='cp1252')

"""