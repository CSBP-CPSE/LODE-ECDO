import pandas as pd
import numpy as np
import sys
import shutil
from hashlib import blake2b
from hashlib import sha256
from tqdm import tqdm

def GetHash(x):
    h = sha256()
    h.update(x.encode())
    return h.hexdigest()

def make_temp_col(df):
    df_temp=df.copy()
    cols=['facility_name','street_name','city','latitude','street_no','longitude','facility_type']
    del_list=["-","'","."]
    for col in cols:
    
        df_temp[col]=df_temp[col].str.upper()
        df_temp[col]=df_temp[col].fillna('NULL')
    
        for i in del_list:
            df_temp[col]=df_temp[col].str.replace(i,'',regex=False)
    df_temp['temp']=df_temp['facility_name']+'-'+df_temp['street_name']+'-'+df_temp['city']+'-'+df_temp['latitude']+'-'+df_temp['street_no']+'-'+df_temp['longitude']+'-'+df_temp['facility_type']
    return df_temp['temp']

def main():
    # Define filepaths
    f_in = "/home/jovyan/ODBiz/4-Parsing/output/2-parsed_biz.csv"
    f_out = "/home/jovyan/ODBiz/4-Parsing/output/parsed_and_combined_biz.csv"
    f_to_geocode = "/home/jovyan/ODBiz/5-Geocoding/data/ODBiz_parsed.csv"

    # Load in the csv
    total_lines = 803584
    chunksize = 10000
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(f_in,
                                        chunksize=chunksize, 
                                        dtype=str), 
                                    desc='Loading data', 
                                    total=total_lines//chunksize+1)
                    ])
    
    # Merge parsed columns with other columns
    df['unit'] = np.nan
    df['street_no'] = df['street_no'].fillna(df['LP2_street_no'])
    df['street_name'] = df['street_name'].fillna(df['LP_street_name'])
    df['postal_code'] = df['postal_code'].fillna(df['LP_PostCode'].str.upper())
    df['city'] = df['city'].fillna(df['LP_City'].str.capitalize())
    df['unit'] = df["LP2_unit"].str.capitalize()
    df['unit'] = df["unit"].fillna(df['LP3_unit'])

    # Reorder columns
    original_cols = df.columns
    dropped_cols = ['LP_street_no', 'LP_street_name', 'LP_City', 'LP_Province',
       'LP_PostCode', 'LP_Unit', 'LP_street_no_alt', 'LP2_unit',
       'LP2_street_no', 'spill', 'LP3_unit', 'parsing_err_exists', 'flagged_parsing_err']
    column_reorder = [
                                        'idx',
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
                                        'postal_code',
                                        'unit',
                                        'street_no',
                                        'street_name',
                                        'street_direction',
                                        'street_type',
                                        'city',
                                        'province',
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
                                        'provider',
                                        'geo_source',
                                        'LP_street_no', #
                                        'LP_street_name',#
                                        'LP_City', #
                                        'LP_Province', #
                                        'LP_PostCode', #
                                        'LP_Unit', #
                                        'LP_street_no_alt', #
                                        'LP2_unit', #
                                        'LP2_street_no', #
                                        'spill', #
                                        'LP3_unit', #
                                        'parsing_err_exists', #
                                        'flagged_parsing_err' #
                                        ]

    # Print out unexpected missing columns
    missing_cols = original_cols[~original_cols.isin(column_reorder)]
    missing_cols = missing_cols[~missing_cols.isin(dropped_cols)]
    if len(missing_cols) != 0:
        print('WARNING! Missing columns!')
        for i in missing_cols:
            print(i)
    df = df[column_reorder]

    # Remove all postal codes that are not 6 characters long and that do not follow the format of a postal code
    df['postal_code'] = df['postal_code'].str.replace(' ','').str.upper()
    df['postal_code'] = df['postal_code'].str.replace('-','').str.upper()
    mask = df['postal_code'].astype(str).str.len() != 6
    df.loc[mask, 'postal_code'] = ''

    #fill NAs in full_address
    df['temporary'] = df['unit'].astype(str)+' '+df['street_no'].astype(str)+' '+df['street_name'].astype(str)
    df['temporary'] = df['temporary'].str.replace('nan','')
    df['full_address'] = df['full_address'].fillna(df['temporary'])
    df = df.drop(['temporary'], axis=1)


    # #Create unique identifiers for each datapoint
    # df['temp']=make_temp_col(df)
    # df['idx']=df['temp'].apply(GetHash)

    # #Any indexes that are the same basically mean that the data points are the same, which is why we drop duplicates
    # df = df.drop_duplicates(subset=['idx'])
    # df = df.drop(['temp'], axis=1)
    # df.insert(0, 'idx', df.pop('idx'))

    # Save to csv and copy over to geocoding
    df.to_csv(f_out, index=False)
    shutil.copyfile(f_out, f_to_geocode)
    # df.to_csv('../5-Geocoding/combined.csv', index=False)

    print(df['idx'].value_counts())

if __name__ == '__main__':
    main()



