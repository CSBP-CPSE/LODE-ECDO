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
from tqdm import tqdm # For status bars

# Memory viewer
# import os, psutil
# process = psutil.Process(os.getpid())
# # print(process.memory_info().rss)  # in bytes 
# ram_time = 10
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
    ET = 'Canada/Eastern'
    start_time = dt.now(timezone(ET))
    today = str(start_time)[:10]

    # File path names
    pdir="/home/jovyan/ODBiz/3-Merging/input"
    outName = f"/home/jovyan/ODBiz/3-Merging/output/ODBiz_merged_{today}"

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

    # List files to exclude from merging (by listing the file names)      
    excluded_files = []

    # Begin merging csvs
    DFS=[]
    files=[f for f in listdir(pdir) if f.endswith('.csv')]
    print('Begin merging files together...')
    for f in tqdm(files):
        if f in excluded_files:
            continue
        df_temp=pd.read_csv(f'{pdir}/{f}',dtype=str, low_memory=False)
        DFS.append(df_temp)

    # Reorder the columns
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
            'country',
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
            'status',
            'provider'
            ]
    df=df_unordered[col_order]

    #standardise province names
    df.loc[df.provider=='Province of Alberta','province']='AB'
    df.loc[df.provider=='Province of British Columbia','province']='BC'
    df.loc[df.provider=='Province of Ontario','province']='ON'
    df.loc[df.provider=='Province of Québec','province']='QC'
    df.loc[df.provider=='Province of Saskatchewan','province']='SK'
    df.loc[df.provider=='Province of Nova Scotia','province']='NS'
    df.loc[df.provider=='Province of Prince Edward Island','province']='PE'

    provs_dict={'Alberta':'AB',
               'British Columbia':'BC',
               '`': 'BC', # 1 business keeps setting their province to ` and I have determined that they’re located in BC
               'Manitoba':'MB',
               'New Brunswick':'NB',
               'Newfoundland and Labrador':'NL',
               'Newfoundland And Labrador':'NL',
               'NF':'NL',
               'Nova Scotia':'NS',
               'Northwest Territories':'NT',
               'Nunavut':'NU',
               'Ontario':'ON',
               'ONTARIO':'ON',
               'Prince Edward Island':'PE',
               'Quebec':'QC',
               'QB':'QC',
               'PQ':'QC',
               'Saskatchewan':'SK',
               'Yukon Territories':'YT',
               'Yukon':'YT'}
    print('Standardizing Province Names...')
    for key in tqdm(provs_dict):
        df['province'] = df['province'].str.replace(key, provs_dict[key],regex=False)
    df['province'] = df['province'].str.upper()

    # Standardize Country Names
    country_dict = {
        '^CA$': 'CANADA'
    }
    print('Standardizing Country Names...')
    for key in tqdm(country_dict):
        df['country'] = df['country'].str.replace(key, country_dict[key], regex = True)
    df['country'] = df['country'].str.upper()
        
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
    print('Making Postal Codes consistent...')
    df['postal_code']=tqdm(df['postal_code'].str.replace(' ','').str.upper())

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
    print('Dropping Duplicates')
    df['duplicated'] = df.duplicated(subset=dup_keys, keep='first')
    dup_exists = True in df['duplicated']
    print(f'Does at least 1 obvious duplicate exist? {dup_exists}')

    # # Drop temp columns
    # df = df.drop(columns = ['is_trade_school', 'duplicated'])

    #finally, replace index with fresh index
    print('Creating idx_basic...')
    df['idx_basic']=tqdm(range(1,1+len(df)))

    def make_temp_col(df):
        df_temp=df.copy()
        cols=dup_keys
        del_list=[" ","-","'","."]
        print('Capitalize values and fill in blanks of dup_key columns with NULL to a copy of the df')
        for col in tqdm(cols):
        
            df_temp[col]=df_temp[col].str.upper()
            df_temp[col]=df_temp[col].fillna('NULL')
        
            for i in del_list:
                df_temp[col]=df_temp[col].str.replace(i,'',regex=False)

        df_temp['temp'] = ''
        print('Appending dup_key columns together and assign to temp column')
        for col in tqdm(cols):
            df_temp['temp'] += df_temp[col] 
            if col != cols[-1]:
                df_temp['temp'] += '-'
        
        # df_temp['temp']=df_temp['source_id']+'-'+df_temp['facility_name']+'-'+df_temp['address_str']+'-'+df_temp['provider']
        return df_temp['temp']

    print('Creating temp column:')
    df['temp']=make_temp_col(df)
    print('Applying hashing to get new indicies...')
    df['idx']=tqdm(df['temp'].apply(GetHash))

    # Fill in geo_source.
    print('Filling in geo_source column')
    if ~('geo_source' in df.columns):
        df['geo_source'] = ''
    df.loc[~df.latitude.isnull() & df.geo_source.isnull(), 'geo_source']='Source'

    # Write dataframe to csv
    print(f'Writing {len(df)} dataframe entries to csv. This will take a while and unfortunately no easy progress bar solutions were available here...')
    df.to_csv(f'{outName}.csv',index=False)
    print(f'File saved to {outName}.csv')
    end_time = dt.now(timezone(ET)) - start_time
    print(f'Finished in {end_time.total_seconds()} seconds')

if __name__ == '__main__':
    main()
