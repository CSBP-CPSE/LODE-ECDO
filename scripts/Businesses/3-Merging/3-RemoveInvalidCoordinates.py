import pandas as pd
import numpy as np
from tqdm import tqdm
from pytz import timezone
from datetime import datetime as dt

def main():
    # Retrieve today's date
    ET = 'Canada/Eastern'
    start_time = dt.now(timezone(ET))
    # today = str(start_time)[:10]
    today = '2022-07-04'

    # File path names
    inputFileName = f"/home/jovyan/ODBiz/3-Merging/output/ODBiz_merged_{today}.csv"
    inv_coords_csv = '/home/jovyan/ODBiz/3-Merging/output/inv_coords_affected_rows.csv'

    # Load in the csv
    total_lines = 1302310
    chunksize = 100000
    # types_dict = {'street_no': str} # Read in street numbers as strs since some of them are formatted weirdly
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(inputFileName, chunksize=chunksize, dtype = str), desc='Loading data', total=total_lines//chunksize)])

    # Remove invalid geo coords
    df[["latitude", "longitude"]] = df[["latitude", "longitude"]].apply(pd.to_numeric, errors = 'coerce')
    df['valid_coord'] = False
    wrong_lons = [123.0058404, 120.8552187]
    for i, row in tqdm(df.iterrows(), total = total_lines, desc='Marking Valid Coordinates'):
        if row['longitude'] in wrong_lons:
            df.loc[i, 'longitude'] = - row['longitude']
            df.loc[i, 'valid_coord'] = True
        elif row['latitude'] > 0 and row['longitude'] < 0 or row['latitude'] is np.nan:
            df.loc[i, 'valid_coord'] = True

    export_idx = False

    # df = df.set_index('idx')
    # export_idx = True

    df_invalid_coords = df[~df['valid_coord']]
    df_invalid_coords.to_csv(inv_coords_csv, index = export_idx)
    print(inv_coords_csv)

    df_invalid_coords['latitude'] = np.nan
    df_invalid_coords['longitude'] = np.nan

    df.merge(df_invalid_coords, how = 'right')
    df.to_csv(inputFileName, index = export_idx)
    print(f'df saved to {inputFileName}')

if __name__ == '__main__':
    main()