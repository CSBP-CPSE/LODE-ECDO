'''
standardize_dates.py

For all datasets that have a `date_established` or equivalent column 
(as determined by variablemap.csv), this script will try to convert the 
date format into YYYY-MM-DD if it's not already in that format. If not
enough info is provided (e.g. only the year is provided), then it will
leave the data as-is.
'''

from datetime import datetime as dt
import pandas as pd 

def standardize_dates(date_series: pd.Series, date_format: str) -> pd.Series:
    '''
    Takes in a series of dates, converts them to strs, then into datetime objects, then back to strs
    Returns a series of strings of the form 'YYYY-MM-DD'
    '''
    
    date_series = date_series.map(str)
    date_series = date_series.map(lambda x: dt.strptime(x, date_format))
    date_series = date_series.map(lambda x: x.strftime('%Y-%m-%d'))

    return date_series

def main():
    # Define file paths
    ODBizSources_path = '/home/jovyan/ODBiz/1-PreProcessing/ODBizSources.csv'
    variablemap_path = '/home/jovyan/ODBiz/2-OpenTabulate/variablemap.csv'
    raw_folder_path = '/home/jovyan/ODBiz/1-PreProcessing/raw'
    processed_folder_path = '/home/jovyan/ODBiz/1-PreProcessing/processed'

    # Load csvs
    df_sources = pd.read_csv(ODBizSources_path)
    df_varmap = pd.read_csv(variablemap_path)
    df_varmap = df_varmap.fillna('')

    # Set indicies
    df_sources = df_sources.set_index('localfile')
    df_varmap = df_varmap.set_index('localfile')

    # Iterate through the rows of varmap
    for i, row in df_varmap.iterrows():
        if row.date_established != '':
            date_format = df_sources.date_format[i]
            # print(i, F'({row.date_established}) :' , date_format)

            if not(date_format in ['%Y-%m-%d', '%Y']):
                # Read in the corresponding csv from raw
                city_df = pd.read_csv(f'{raw_folder_path}/{i}', keep_default_na = False)
                old_dates = city_df[row.date_established]
                new_dates = standardize_dates(old_dates, date_format)
                city_df[row.date_established] = new_dates
                city_df.to_csv(f'{processed_folder_path}/{i}')
                print(f'Updated {processed_folder_path}/{i}')

if __name__ == '__main__':
    main()