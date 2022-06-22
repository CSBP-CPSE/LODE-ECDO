'''
merging_biz.py

This script reads in, then merges all the output data from the 2-OpenTabulate/Output folder except for specified excluded files. 

This script also standardizes the following values:
    - NAICS values
    - province names
    - Telephone?
    - ...

This script also filters out datasets of the following criteria:
    - ...
    
A unique index is generated and assigned to every entry to help with data processing further along the pipeline beyond this point.
    
Output:
A .csv file, both containing the same merged data.
'''

# Import required packages
import pandas as pd
from os import listdir
from hashlib import blake2b
from datetime import datetime as dt
from pytz import timezone
import openpyxl

# Memory viewer
import os, psutil
process = psutil.Process(os.getpid())
# print(process.memory_info().rss)  # in bytes 
ram_time = 10
# print(psutil.cpu_percent(ram_time))

def GetHash(x):
    '''
    Output the hash of the string x
    '''
    h=blake2b(digest_size=10)
    h.update(x.encode())
    return h.hexdigest()

def main():
    # Retrieve today's date
    # today = dt.date.today()
    today = dt.now(timezone('Canada/Eastern'))
    today = str(today)[:10]

    # File path names
    pdir="/home/jovyan/ODBiz/2-OpenTabulate/data/output"
    outName = f"/home/jovyan/ODBiz/3-Merging/ODBiz_merged_{today}"

    # Duplicate keys
    # Use these columns to determine obvious duplicates and 
    # to generate our indices
    dup_keys = ['business_name',
                'licence_number',
                'business_id_no',
                'primary_NAICS',
                'full_address',
                'full_address_2',
                'province'
                ]
                    
    #read in all parsed files and concatenate together
    # sources=['ab','bc','mb','nb','nl','ns','nt','nu','on','pe','qc','sk','yt', 'supplementary_files'#,'esdc'
    # 		]
    excluded_files = []

    DFS=[]
    # for s in sources:
    files=[f for f in listdir(pdir) if f.endswith('.csv')]
    for f in files:
        if f in excluded_files:
            continue
        # df_temp=pd.read_csv("{}/{}/{}".format(pdir,s,f),dtype=str, low_memory=False)
        df_temp=pd.read_csv(f'{pdir}/{f}',dtype=str, low_memory=False)
        DFS.append(df_temp)

    print('A')
    df_unordered=pd.concat(DFS, ignore_index = True)
    del DFS
    col_order = [ 'idx',
            'localfile',
            'business_name',
            'business_sector',
            'business_subsector',
            'business_description',
            'business_id_no',
            'licence_number',
            'licence_type',
            'primary_NAICS',
            'secondary_NAICS',
            'NAICS_descr',
            'alt_econ_act_code',
            'alt_econ_act_descrip',
            'latitude',
            'longitude',
            'full_address',
            'full_address_2',
            'mailing_address',
            'unit',
            'street_no',
            'street_name',
            'street_direction',
            'street_type',
            'city',
            'province',
            'postal_code',
            'business_website',
            'email',
            'telephone',
            'telephone_extension',
            'toll_free_telephone',
            'fax',
            'total_no_employees',
            'no_full_time',
            'no_part_time',
            'no_seasonal',
            'date_established',
            'indigenous',
            'provider'
            ]
    # test = -39
    # print(col_order[test])
    print('B')
    # print(psutil.cpu_percent(ram_time))  # in bytes 
    df = pd.DataFrame()
    for i in col_order:
        print(i)
        df[i]=df_unordered[i]
        del df_unordered[i]
    # df=df_unordered[col_order]
    print('C')
    # print(psutil.cpu_percent(ram_time))  # in bytes 

    # #standardise ISCEDs:
    # ISCEDS=['ISCED010','ISCED020','ISCED1','ISCED2','ISCED3','ISCED4+',]
    # for I in ISCEDS:
    #     df[I]=df[I].str.replace('Y','1', regex=False)
    #     df[I]=df[I].str.replace('N','0', regex=False)
    #     df[I]=df[I].str.replace('1.0','1', regex=False)
    #     df[I]=df[I].str.replace('0.0','0', regex=False)

    # #standardise province names
    # df.loc[df.provider=='Province of Alberta','province']='AB'
    # df.loc[df.provider=='Province of British Columbia','province']='BC'
    # df.loc[df.provider=='Province of Ontario','province']='ON'
    # df.loc[df.provider=='Province of Québec','province']='QC'
    # df.loc[df.provider=='Province of Saskatchewan','province']='SK'
    # df.loc[df.provider=='Province of Nova Scotia','province']='NS'
    # df.loc[df.provider=='Province of Prince Edward Island','province']='PE'

    # provs_dict={'Alberta':'AB',
    #            'British Columbia':'BC',
    #            'Manitoba':'MB',
    #            'New Brunswick':'NB',
    #            'Newfoundland and Labrador':'NL',
    #            'Nova Scotia':'NS',
    #            'Northwest Territories':'NT',
    #            'Nunavut':'NU',
    #            'Ontario':'ON',
    #            'Prince Edward Island':'PE',
    #            'Quebec':'QC',
    #            'Saskatchewan':'SK',
    #            'Yukon Territories':'YT',
    #            'Yukon':'YT'}


    # for key in provs_dict:
    #     df['province'] = df['province'].str.replace(key, provs_dict[key],regex=False)
        
    # #standardise language entries
    # df['language']=df['language'].str.replace('Intensive French Integrated French','French', regex=False)
    # df['language']=df['language'].str.replace('Late Immersion Integrated French','French', regex=False)
    # df['language']=df['language'].str.replace('Intensive French Intergrated French','French', regex=False)
    # df['language']=df['language'].str.replace('Francophone','French', regex=False)
    # df['language']=df['language'].str.replace('French','French', regex=False)
    # df['language']=df['language'].str.replace('Intensive French','French', regex=False)
    # df['language']=df['language'].str.replace('Integrated French','French', regex=False)
    # df['language']=df['language'].str.replace('Intergrated French','French', regex=False)
    # df['language']=df['language'].str.replace('Inregrated French','French', regex=False)
    # df['language']=df['language'].str.replace('Franco','French', regex=False)
    # df['language']=df['language'].str.replace('Anglo','English', regex=False)
    # # raise NotImplementedError('Language standardization not yet implemented')
        
    # #fix NS city field with "NS" appended to it
    # df.loc[df.province=='NS','city']=df.loc[df.province=='NS','city'].str.rstrip(' NS')

    #make postal codes consistent
    df['postal_code']=df['postal_code'].str.replace(' ','').str.upper()

    # #excel turns grade ranges with hyphens to dates, so replace with double hyphens
    # df['grade_range']=df['grade_range'].str.replace('-','--')
    # df['grade_range']=df['grade_range'].str.replace('---','--')
    # df['grade_range']=df['grade_range'].str.replace('Pre--K','Pre-K')

    # #Drop entries that shouldn't be included
    # drop_list=['Home-based School', 'Home Based School', 'StrongStart BC']

    # for d in drop_list:
    #     df.drop(df.loc[df['facility_name']==d].index, inplace=True)
        
    # # If the school doesn't offer K--12 education, drop it
    # df['is_trade_school'] = False
    # grade_cols = ['ISCED020','ISCED1','ISCED2','ISCED3']
    # for i, row in df.iterrows():
    #     sum_so_far = 0
    #     for j in row[grade_cols]:
    #         if not(pd.isna(j)):
    #             sum_so_far += int(j)
    # #     print(sum_so_far)
    #     if sum_so_far == 0:
    # #         print(i)
    #         df.loc[i, 'is_trade_school'] = True
            
    # df.drop(df.loc[df['is_trade_school']==True].index, inplace=True)
        
    # # Drop adult schools
    # qc_adult_schools = '9_OrgImm_Anglo_Adu'
    # df.drop(df.loc[df['facility_type']==qc_adult_schools].index, inplace=True)

    # Drop duplicates
    df['duplicated'] = df.duplicated(subset=dup_keys, keep='first')
    dup_exists = True in df['duplicated']
    print(f'Does at least 1 obvious duplicate exist? {dup_exists}')

    # # Drop temp columns
    # df = df.drop(columns = ['is_trade_school', 'duplicated'])

    #finally, replace index with fresh index
    df['idx_basic']=range(1,1+len(df))

    def make_temp_col(df):
        df_temp=df.copy()
        cols=dup_keys
        del_list=[" ","-","'","."]
        for col in cols:
        
            df_temp[col]=df_temp[col].str.upper()
            df_temp[col]=df_temp[col].fillna('NULL')
        
            for i in del_list:
                df_temp[col]=df_temp[col].str.replace(i,'',regex=False)

        df_temp['temp'] = ''
        for col in cols:
            df_temp['temp'] += df_temp[col] 
            if col != cols[-1]:
                df_temp['temp'] += '-'
        
        # df_temp['temp']=df_temp['source_id']+'-'+df_temp['facility_name']+'-'+df_temp['address_str']+'-'+df_temp['provider']
        return df_temp['temp']

    df['temp']=make_temp_col(df)
    df['idx']=df['temp'].apply(GetHash)

    #fill in geo_method.
    if ~('geo_source' in df.columns):
        df['geo_source'] = ''
    df.loc[~df.latitude.isnull() & df.geo_source.isnull(), 'geo_source']='Source'

    #print(len(df), 'entries in database')

    # Write dataframe to csv
    df.to_csv(f'{outName}.csv',index=False)
    print(f'File saved to {outName}.csv')
    print('Done')

if __name__ == '__main__':
    main()
