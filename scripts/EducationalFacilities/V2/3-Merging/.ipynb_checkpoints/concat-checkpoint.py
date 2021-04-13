import pandas as pd
from os import listdir
from hashlib import blake2b

def GetHash(x):
    h=blake2b(digest_size=10)
    h.update(x.encode())
    return h.hexdigest()


#read in all parsed files and concatenate together
pdir="/home/jovyan/data-vol-1/ODEF/2-opentabulate/data/output"

sources=['ab','bc','mb','nb','nl','ns','nt','nu','on','pe','qc','sk','yt','esdc']
DFS=[]
for s in sources:
    files=[f for f in listdir("{}/{}".format(pdir,s)) if f.endswith('.csv')]
    for f in files:
        df_temp=pd.read_csv("{}/{}/{}".format(pdir,s,f),dtype=str, low_memory=False)
        DFS.append(df_temp)

df=pd.concat(DFS)

df=df[['idx', 'source_id','facility_name', 'facility_type','authority_name','authority_type', 'grade_range','grade_type','ISCED010', 'ISCED020','ISCED1', 'ISCED2', 'ISCED3', 'ISCED4+', 'address_str',   'street_addr', 'city', 'province', 'postal_code', 'provider', 'latitude', 'longitude','geo_source', 'telephone' ]]

#standardise ISCEDs:
ISCEDS=['ISCED010','ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+',]
for I in ISCEDS:
    df[I]=df[I].str.replace('Y','1', regex=False)
    df[I]=df[I].str.replace('N','0', regex=False)
    df[I]=df[I].str.replace('1.0','1', regex=False)
    df[I]=df[I].str.replace('0.0','0', regex=False)

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
    
#fix NS city field with "NS" appended to it

df.loc[df.province=='NS','city']=df.loc[df.province=='NS','city'].str.rstrip(' NS')

#make postal codes consistent

df['postal_code']=df['postal_code'].str.replace(' ','').str.upper()

#excel turns grade ranges with hyphens to dates, so replace with double hyphens

df['grade_range']=df['grade_range'].str.replace('-','--')
df['grade_range']=df['grade_range'].str.replace('---','--')
df['grade_range']=df['grade_range'].str.replace('Pre--K','Pre-K')

#Drop entries that shouldn't be included

drop_list=['Home-based School']

for d in drop_list:
    df.drop(df.loc[df['facility_name']==d].index, inplace=True)
    

#finally, replace index with fresh index

df['idx_basic']=range(1,1+len(df))

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

#print(len(df), 'entries in database')

#check total against all input files
"""
all_files=[
"/home/jovyan/data-vol-1/opentabulate/data/output/ab/AB_authority_and_school.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/bc/excelSchoolContact_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/mb/Schools in MB Jan 2019_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/nb/NB_AlternativeLearningCentre_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/nb/NB_ExternalServiceFacilities.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/nb/NB_FirstNationsSchools_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/nb/NB_PublicSchools_geonb_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/nl/nl_allschools1920_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/ns/Recognized_Private_Schools_Granting_the_Nova_Scotia_High_School_Leaving_Certificate_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/ns/directoryofpublicschools2019-2020_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/nt/NT-education_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/nu/NU-education.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/on/on_private_schools_contact_information_october_2020_en_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/on/new_sif_data_table_2018_2019prelim_en_september_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/pe/OD0055_Public_School_Locations.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/qc/PPS_Prive_Installation_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/qc/ES_Collegial.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/qc/ES_Universitaire.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/qc/PPS_Gouvernemental_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/sk/sk_ActiveListofSchoolDivisionSchools_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/yt/yt-education-2_isced.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/NL-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/NT-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/NB-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/MB-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/BC-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/SK-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/YT-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/AB-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/PE-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/NS-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/QC-esdc.csv",
"/home/jovyan/data-vol-1/opentabulate/data/output/esdc/ON-esdc.csv"
]
df_q1=pd.read_csv("/home/jovyan/data-vol-1/opentabulate/data/input/qc/PPS_Public_Immeuble_isced.csv")
df_q1=df_q1.dropna(subset=["ORDRE_ENS"])
df_q1=df_q1.loc[df_q1["STAT_PROP_IMM"]== "Propriété de la CS"]

N1=len(df_q1)
for f in all_files:
    temp=pd.read_csv(f)
    N1+=len(temp)

print(N1)
print(len(df))

#test checks out

"""
df.to_csv('ODEFv2_31-03-2021.csv',index=False)
