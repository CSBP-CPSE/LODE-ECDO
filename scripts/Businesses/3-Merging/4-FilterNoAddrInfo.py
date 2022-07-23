import pandas as pd
import numpy as np
from tqdm import tqdm
from pytz import timezone
from datetime import datetime as dt

def check_addr_info(row):
    '''FIGURE OUT HOW TO IMPLEMENT THIS FUNCTION TO BE USED WITH APPLY!
    '''
    # df_lon = df['longitude']
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
    if row['latitude'] == '':
        addr_info = row.loc[addr_keys]
        addr_info = addr_info.values
        addr_info = ''.join(addr_info)
        if addr_info == '':
            # Mark this business for removal!
            return False
    return True


def main():
    # Retrieve today's date
    ET = 'Canada/Eastern'
    start_time = dt.now(timezone(ET))
    today = str(start_time)[:10]
    inputFileDate = '2022-07-04'

    # File path names
    inputFileName = f"/home/jovyan/ODBiz/3-Merging/output/3-ODBiz_merged_{inputFileDate}.csv"
    inputFileName = f"/home/jovyan/ODBiz/3-Merging/output/ODBiz_merged_{inputFileDate}.csv"
    outputFileName = f"/home/jovyan/ODBiz/3-Merging/output/4-ODBiz_merged_{today}.csv"

    # Load in the csv
    total_lines = 1302310
    chunksize = 100000
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(inputFileName, chunksize=chunksize, dtype = str), desc='Loading data', total=total_lines//chunksize)])
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
    df = df[df['has_addr_info'] == True]
    old_time = new_time
    new_time = dt.now(timezone(ET))
    exetime = new_time - old_time
    print(f'Done in {exetime.seconds} s')

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