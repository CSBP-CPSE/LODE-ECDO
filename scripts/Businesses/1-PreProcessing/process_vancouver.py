'''
process_vancouver.py

The BC_Vancouver_Business_Licences.csv dataset had an intense cleaning process.
Modifications made to the Vancouver dataset include:
1. Filtering out all non-Canadian business (determined by location of HQ)
2. Extracting lat/lon coordinates from JSON str format
3. Creating a new column to more accurately record the business names of each business.
'''

import numpy as np
import pandas as pd 
from tqdm import tqdm

def strip_point(x: str) -> list: 
    '''
    Converts a JSON formatted geomarker into a (lon, lat) list.

    Arguments:
        - x (str): A JSON string containing the lat/lon coordinates of the business
    
    Returns:
        - A list of 2 strings [lon, lat]
    '''  
    try:
        t = x.strip(r'{""coordinates"": [')
        t = t.rstrip('], ""type"": ""Point""}')
        t = t.replace(',', '')
        return t.split()
    except:
        return np.nan

def main():
    # Define file path names
    inputFileName = '/home/jovyan/ODBiz/1-PreProcessing/raw/BC_Vancouver_Business_Licences.csv'
    outputFileName = '/home/jovyan/ODBiz/1-PreProcessing/processed/BC_Vancouver_Business_Licences.csv'

    # Load in the csv
    df = pd.read_csv(inputFileName, low_memory=False)
    total_lines = 636855
    chunksize = 1000
    # df = pd.read_csv(mergedFilePathName, low_memory=False)
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(inputFileName, chunksize=chunksize), desc='Loading data', total=total_lines//chunksize+1)])

    # Filter out non-Canadian businesses
    nonCAD_provs = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
            'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
            'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
            'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
            'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY', 
            # 'LAKEVIEW ESTATES',
            'TEHRAN',
            'CHESHITE',
            'ARIZONA', 
            'US', 'HB', 'SP', 'RJ'
            ]
    df = df[~(df['Province'].str.upper().isin(nonCAD_provs))]
            
    # BC vancouver lat/long
    LONGS=[]
    LATS=[]
    for i in tqdm(df["Geom"], desc='Extracting geocoordinates'):
        try:
            stripped_point = strip_point(i)
            LONGS.append(stripped_point[0])
            LATS.append(stripped_point[1])
        except:
            LONGS.append(np.nan)
            LATS.append(np.nan)

    df["long"]=LONGS
    df["lat"]=LATS

    # Creating a new column to more accurately record the business names of each business
    df['business_name'] = df['BusinessName']
    df['business_name'] = df['business_name'].fillna('')
    df['BusinessTradeName'] = df['BusinessTradeName'].fillna('')
    row_count = df.shape[0]
    for i, row in tqdm(df.iterrows(), desc='Creating new business_name column', total=row_count):
        business_name = row['business_name']
        if business_name != '':
            first_char = business_name[0]
            last_char = business_name[-1]
            if first_char == '(' and last_char == ')' and df.loc[i, 'BusinessTradeName'] != '':
                # print(df.loc[i, 'BusinessTradeName'])
                df.loc[i, 'business_name'] = df.loc[i, 'BusinessTradeName']
        else:
            df.loc[i, 'business_name'] = df.loc[i, 'BusinessTradeName']
    df.to_csv(outputFileName)
    print(f'File saved to {outputFileName}')

if __name__ == '__main__':
    main()