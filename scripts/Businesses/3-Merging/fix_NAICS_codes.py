'''
fix_NAICS_codes.py

Removes trailing zeros for all primary NAICS code values with strictly less than 6 digits
This is because those NAICS codes would cause NAICS queries to return empty
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

    # File path names
    inputFileName = f"/home/jovyan/ODBiz/3-Merging/output/3-ODBiz_merged_{inputFileDate}.csv"
    outputFileName = f"/home/jovyan/ODBiz/3-Merging/output/4-ODBiz_merged_{today}.csv"
    
    # Load in the csv
    total_lines = 802383 
    chunksize = 100000
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(inputFileName, chunksize=chunksize, dtype = str), desc='Loading data', total=total_lines//chunksize+1)])
    print(f'Loaded in        {df.shape[0]} rows')

    # Remove invalid NAICS values
    df['primary_NAICS'] = df['primary_NAICS'].str.replace('.0', '', regex = False)
    df['primary_NAICS'] = df['primary_NAICS'].replace('TBD', np.nan, regex = False)
    df['primary_NAICS'] = df['primary_NAICS'].replace('tbd', np.nan, regex = False)
    df['primary_NAICS'] = df['primary_NAICS'].replace('-', np.nan, regex = False)
    df['primary_NAICS'] = df['primary_NAICS'].str.replace(r'\s\-\s.*', '', regex = True)
    df['primary_NAICS'] = df['primary_NAICS'].astype('Int64')
    df['primary_NAICS'] = df['primary_NAICS'].abs()

    # Trailing zero and strictly less than 6 digits results in empty query, truncate!
    df['invalid_NAICS_query'] = (df['primary_NAICS'] % 10 == 0) & (df['primary_NAICS'] // 100000 == 0)
    df.loc[df['invalid_NAICS_query'] == True, 'primary_NAICS'] = df.loc[df['invalid_NAICS_query'] == True, 'primary_NAICS']//10

    # Drop the temp columns
    df = df.drop('invalid_NAICS_query', axis = 'columns')

    # Save df to file
    df.to_csv(outputFileName, index = False)
    print(f'Resulting df has {df.shape[0]} rows')
    print(f'File saved to {outputFileName}')

    # Display execution time
    end_time = dt.now(timezone(ET))
    exetime = end_time - start_time
    print(f'Execution finished in {exetime.seconds} s')

if __name__ == '__main__':
    main()