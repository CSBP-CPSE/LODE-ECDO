'''
FilterNoAddrInfo.py

Filters out entries with insufficient address info for geocoding
'''

import pandas as pd
import numpy as np
from tqdm import tqdm
from pytz import timezone
from datetime import datetime as dt

def main():
    # Retrieve today's date
    ET = 'Canada/Eastern'
    start_time = dt.now(timezone(ET))
    today = str(start_time)[:10]
    inputFileDate = today
    # inputFileDate = '2022-07-04'

    # File path names
    inputFileName = f"/home/jovyan/ODBiz/3-Merging/output/2-ODBiz_merged_{inputFileDate}.csv"
    outputFileName = f"/home/jovyan/ODBiz/3-Merging/output/3-ODBiz_merged_{today}.csv"
    df_no_info_path = f'/home/jovyan/ODBiz/3-Merging/double_check/no_addr_info.csv'

    # Load in the csv
    total_lines = 802564 
    chunksize = 100000
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(inputFileName, chunksize=chunksize, dtype = str), desc='Loading data', total=total_lines//chunksize+1)])
    print('Filling in NA as empty string')
    old_time = dt.now(timezone(ET))
    df = df.fillna('')
    new_time = dt.now(timezone(ET))
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    # Check each row to see if there's are addresses/geocoord info
    print('Concatenating address info')
    addr_keys = ['full_address',
                    'full_address_2',
                    'mailing_address',
                    'unit',
                    'street_no',
                    'street_name',
                    'street_direction',
                    'street_type',
                    'city',
                    'postal_code']
    df['addr_info'] = df[addr_keys].agg('_'.join, axis = 1, )
    old_time = new_time
    new_time = dt.now(timezone(ET))
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')
    
    # Mark entries with insufficient address info
    print('Checking for blanks')
    blank_match = '_' * (len(addr_keys)-1)
    df['has_addr_info'] = df['addr_info'] != blank_match
    old_time = new_time
    new_time = dt.now(timezone(ET))
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')
    
    # Drop entries with insufficient address info
    print('Dropping entries with insufficient address info')
    df_no_info = df[df['has_addr_info'] == False]
    df_no_info.to_csv(df_no_info_path, index = False)
    print(f'Saving df_no_info to {df_no_info_path}')

    df = df[df['has_addr_info'] == True]
    old_time = new_time
    new_time = dt.now(timezone(ET))
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

    # Drop the temp columns
    df = df.drop(['addr_info', 'has_addr_info'], axis = 'columns')

    # Save the df to csv
    print(f'Saving df to {outputFileName}')
    df.to_csv(outputFileName, index = False)
    old_time = new_time
    new_time = dt.now(timezone(ET))
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')
    print(f'df saved to {outputFileName}')

if __name__ == '__main__':
    main()