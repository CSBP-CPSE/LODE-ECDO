"""
This script fixes errors in parsing by libpostal by identifying street_no entries with multiple numbers or non-numeric characters,
and also allows for manual fixes to entries, which may necessitate re-computing the hash in some cases for the id (if the name or address field changes)
"""

from hashlib import blake2b
import pandas as pd


def GetHash(x):
    h=blake2b(digest_size=10)
    h.update(x.encode())
    return h.hexdigest()


df=pd.read_csv('../7-Deduplication/output/ODEFv2_DupesDropped_07-04-2021.csv',low_memory=False,dtype='str', index_col="Index")
"""
First, deal with incorrect parsings. We can fix the easy ones, where the name has been parsed to "street" or "ave" in an automated way
Those that have multiple entries, or weird entries in street_no otherwise, can have all parsed info deleted.
"""

df['Street_Name']=df['Street_Name'].str.replace('.','',regex=False)
df['Street_No']=df['Street_No'].str.replace('-',' ',regex=False)
df['Street_No']=df['Street_No'].str.replace(' +',' ', regex=True)

#loop through street no to where there are multiple numbers separated by space, and where street_name is "street", "avenue", etc

street_name=list(df['Street_Name'].fillna(''))
street_no=list(df['Street_No'].fillna('').astype(str))
unit=list(df['Unit'].fillna(''))

#make a combination of common street names and directions
streets=['street','st','ave','av','avenue']

dirs=['n',
     'e',
     'w',
     's',
     'ne',
     'nw',
     'se',
     'sw']

checks = streets.copy()

for i in streets:
    for j in dirs:
        checks.append("{} {}".format(i,j))
        

for i in range(len(df)):
    N=street_no[i].split(' ')
    
    if len(N)==2:
        if street_name[i] in(checks):
            new_name="{} {}".format(N[1], street_name[i])
            street_name[i]=new_name
            street_no[i]=N[0]
            unit[i]=''
        else:
            street_name[i]=''
            street_no[i]=''
            unit[i]=''
    elif len(N)==3:
            
        if street_name[i] in(checks):
            new_name="{} {}".format(N[2], street_name[i])
            street_name[i]=new_name
            street_no[i]=N[1]
            unit[i]=N[0]
            
        else:
            street_name[i]=''
            street_no[i]=''
            unit[i]=''
    elif len(N)>3:
        street_name[i]=''
        street_no[i]=''
        unit[i]=''

df['Street_Name']=street_name
df['Street_No']=street_no
df['Unit']=unit


"""
Some entries, particularly in the territories, seem to have broken encodings. We can fix names by ID.

"""


corr=pd.read_csv("Name_Corrections.csv")
df.loc[list(corr['Index']),'Facility_Name']=list(corr["Name"])
df.loc[list(corr['Index']),'Full_Addr']=list(corr["Address"])

corr2=pd.read_csv("Parsing_Corrections.csv")
df.loc[list(corr2['Index']),'Street_No']=list(corr2["street_no"])
df.loc[list(corr2['Index']),'Street_Name']=list(corr2["street_name"])


#fill nulls with '..'
df=df.fillna('..')
df.to_csv("output/ODEFv2_en_07-04-2021.csv")

#make french version of dataset

lang_map={"Facility_Name": "Nom établissement",
         "Facility_Type": "Type_établissement",
         "Authority_Name": "Nom_autorité",
         "ISCED010": "CITE010",
         "ISCED020": "CITE020",
         "ISCED1": "CITE1",
         "ISCED2": "CITE2",
         "ISCED3": "CITE3",
         "ISCED4Plus": "CITE4Plus",
         "Full_Addr": "adr_complète",
         "Street_No": "Numéro_rue",
         "Street_Name": "Nom_rue",
         "Unit": "Unité",
         "City": "Ville",
         "Postal_Code": "Code_postale",
         "Provider": "Fournisseur",
         "CSDUID": "SDRIDU",
         "CSDNAME": "SDR_nom",
         "PRUID": "PRIDU"}
        


df=df.rename(columns=lang_map)

df.to_csv("output/ODEFv2_fr_07-04-2021.csv")

