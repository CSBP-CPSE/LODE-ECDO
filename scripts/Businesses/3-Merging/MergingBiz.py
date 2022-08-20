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
    print('----------------------------------------------------------------------------------------------------------------------------')
    # Toggle a "double checking" mode
    double_check_mode = True

    # Retrieve today's date
    # today = dt.date.today()
    ET = 'Canada/Eastern'
    start_time = dt.now(timezone(ET))
    today = str(start_time)[:10]

    # File path names
    pdir="/home/jovyan/ODBiz/3-Merging/input"
    outName = f"/home/jovyan/ODBiz/3-Merging/output/1-ODBiz_merged_{today}"
    csv_rows_path = f'/home/jovyan/ODBiz/3-Merging/double_check/csv_rows'
    std_prov_path = f'/home/jovyan/ODBiz/3-Merging/double_check/standardized_province_names.csv'
    dups_only_path = f"/home/jovyan/ODBiz/3-Merging/double_check/ODBiz_dups_only.csv"

    if double_check_mode:
        csv_rows_cols = ['localfile', 'num_rows']
        csv_rows_df = pd.DataFrame(columns = csv_rows_cols)

    # Duplicate keys
    # Use these columns to determine obvious duplicates and 
    # to generate our indices
    dup_keys = ['business_name',
                'licence_number',
                'business_id_no',
                'primary_NAICS',
                'full_address',
                'full_address_2',
                'province',
                'business_sector',
                'licence_type'
                ]

    # List files to exclude from merging (by listing the file names)      
    excluded_files = []

    # Begin merging csvs
    DFS=[]
    files=[f for f in listdir(pdir) if f.endswith('.csv')]
    for f in tqdm(files, desc='Merging files'):
        if f in excluded_files:
            continue
        df_temp=pd.read_csv(f'{pdir}/{f}',dtype=str, low_memory=False)
        DFS.append(df_temp)

        # Count the number of rows in each csv
        if double_check_mode:
            num_rows = df_temp.shape[0]
            new_row = pd.DataFrame(data = {'localfile': [f], 'num_rows': [num_rows]})
            csv_rows_df = pd.concat([csv_rows_df,new_row])

    if double_check_mode:
        new_row = pd.DataFrame(data = {'localfile': ['Total'], 'num_rows': [csv_rows_df['num_rows'].sum()]})
        csv_rows_df = pd.concat([csv_rows_df,new_row])
        csv_rows_df.to_csv(f'{csv_rows_path}.csv', index = False)
        print(f'File saved to {csv_rows_path}.csv')
        csv_rows_df = csv_rows_df.sort_values('num_rows', ascending = False)
        csv_rows_df.to_csv(f'{csv_rows_path}_sorted.csv', index = False)
        print(f'File saved to {csv_rows_path}_sorted.csv')


    # Reorder the columns
    print('Reordering columns...')
    old_time = dt.now()
    df_unordered=pd.concat(DFS, ignore_index = True)
    del DFS
    col_order = [ 'idx',
            'localfile',
            'business_name',
            'alt_business_name',
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
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    # Standardize province names
    print('Standardizing Province Names...')

    provs_dict={
                'Province of Alberta': 'AB',
                'Province of British Columbia': 'BC',
                'Province of Ontario': 'ON',
                'Province of Québec': 'QC',
                'Province of Saskatchewan': 'SK',
                'Province of Nova Scotia': 'NS',
                'Province of Prince Edward Island': 'PE',
                'Alberta':'AB',
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

    df['province'] = df['province'].replace(provs_dict)
    df['province'] = df['province'].str.upper()
    if double_check_mode:
        std_prov_df = pd.DataFrame({'post_standarization_count': df['province'].value_counts()})
        std_prov_df.index.name = 'prov_code'
        std_prov_df.to_csv(std_prov_path)
        print(f'File saved to {std_prov_path}')
    old_time = new_time
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    # Standardize Country Names
    print('Standardizing Country Names...')
    country_dict = {
        '^CA$': 'CANADA'
    }
    for key in (country_dict):
        df['country'] = df['country'].str.replace(key, country_dict[key], regex = True)
    df['country'] = df['country'].str.upper()
    old_time = new_time
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    #make postal codes consistent
    print('Making Postal Codes consistent...')
    df['postal_code']=(df['postal_code'].str.replace(' ','').str.upper())
    old_time = new_time
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    # #excel turns ranges with hyphens to dates, so replace with double hyphens
    print('Fixing hyphens...')
    df['unit']=df['unit'].str.replace('-','--')
    df['unit']=df['unit'].str.replace('---','--')
    df['total_no_employees']=df['total_no_employees'].str.replace('-','--')
    df['total_no_employees']=df['total_no_employees'].str.replace('---','--')
    old_time = new_time
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    #finally, replace index with fresh index
    df['idx_basic']=range(1,1+len(df))

    def make_temp_col(df):
        print('Creating temp column:')
        df_temp=df.copy()
        cols=dup_keys
        # del_list=[" ","-","'","."]
        del_list = r"[\s\-'\.]" # Regex equivalent of above (this is faster)
        
        for col in tqdm(cols, desc='Capitalize values and remove punctuation characters'):
            df_temp[col]=df_temp[col].str.upper() # ~ 1.5s
            df_temp[col]=df_temp[col].str.replace(del_list,'',regex=True) # ~ 2s
        
        print('Fill blanks with NULL...')
        old_time = dt.now()
        df_temp[cols]=df_temp[cols].fillna('NULL') # ~ 5s
        new_time = dt.now()
        exetime = new_time - old_time
        print(f'Done in {exetime.seconds} s')

        df_temp['temp'] = ''
        for col in tqdm(cols, desc='Appending dup_key columns together and assign to temp column'):
            df_temp['temp'] += df_temp[col] 
            if col != cols[-1]:
                df_temp['temp'] += '-'
        
        return df_temp['temp']

    df['temp']=make_temp_col(df)
    print('Applying hashing to get new indicies...')
    df['idx']=(df['temp'].apply(GetHash))

    # Fill in geo_source.
    print('Filling in geo_source column')
    if ~('geo_source' in df.columns):
        df['geo_source'] = ''
    df.loc[~df.latitude.isnull() & ((df.geo_source.isnull()) | (df.geo_source == '')), 'geo_source']='Source'

    # Mark duplicates
    print('Marking Duplicates...')
    old_time = dt.now()
    dup_keys = 'idx'
    df['duplicated'] = df.duplicated(subset=dup_keys, keep='first')
    dup_count = df['duplicated'].sum()
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    # Drop duplicates
    print('Dropping duplicates')
    old_time = dt.now()
    df_dups_only = df[df.duplicated(subset=dup_keys, keep=False)]
    df = df.drop_duplicates(dup_keys)
    print(f'{dup_count} duplicate rows dropped')
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    # Remove temporary columns
    df = df.drop(   labels = [  'duplicated',
                                'idx_basic',
                                'temp'], 
                    axis = 'columns')

    # Write dataframe to csv
    print(f'Writing {len(df)} dataframe entries to csv. This will take a while and unfortunately no easy progress bar solutions were available here...')
    old_time = dt.now()
    df_dups_only.to_csv(f'{dups_only_path}',index=False)
    print(f'Duplicates only csv saved to {dups_only_path}')
    df.to_csv(f'{outName}.csv',index=False)
    print(f'File saved to {outName}.csv')
    new_time = dt.now()
    exetime = new_time - old_time
    print(f'csv took {exetime.seconds} s to save')
    tot_exe_time = dt.now(timezone(ET)) - start_time
    print(f'Execution finished in {tot_exe_time.total_seconds()} seconds')

if __name__ == '__main__':
    main()
