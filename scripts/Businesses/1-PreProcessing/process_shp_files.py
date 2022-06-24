'''
process_shp_files.py

Converts .shp files into .csv files.
All shape file variable names are truncated to 10 characters.
This script uses supplementary .csv files that come along with the .shp files 
in order to correct all variable names.
'''

import os
import geopandas as gpd
import pandas as pd

# Global variables
raw_shp_dir = '/home/jovyan/ODBiz/1-PreProcessing/raw/shapefiles'
out_dir = '/home/jovyan/ODBiz/1-PreProcessing' # Default
# out_dir = '/home/jovyan/ODBiz/1-PreProcessing/testing_for_shp_files' 

def shared_prefix(str1: str, str2: str) -> int:
    '''
    Outputs n, where n is the first n characters shared between two strings
    '''
    min_len = min(len(str1), len(str2))
    for i in range(1, min_len+1):
        if str1[:i] != str2[:i]:
            return i-1
    return min_len

def fix_variable_names(gdf: gpd.GeoDataFrame, root: str, name: str) -> gpd.GeoDataFrame:
    '''
    Reads in the corresponding csv file to fix the variable names of the shp file

    Arguments:
    - gdf (GeoDataFrame): A geopandas dataframe that represents the shp file
    - root (str): The directory that the shp file resides in
    - name (str): The name of the file that will be produced

    Returns:
    A GeoDataFrame with the corrected column names
    '''

    # Was for testing, forgot to remove, probably not necessary
    if root == '/home/jovyan/ODBiz/1-PreProcessing/raw/shapefiles/BC_Squamish_shapefile':
        print('')

    # Load in the column names
    df = pd.read_csv(f'{root}/{name}.csv')
    df_cols = df.columns

    # Drop the columns ['X','Y'] if present as these often shift 
    # over the order of the columns
    try:
        df_cols = df_cols.drop(['X','Y'])
    except:
        pass
    gdf_cols = gdf.columns

    # Generate the mapping dict
    rename_dict = {}
    cols_iter = zip(df_cols, gdf_cols)
    for i,j in cols_iter:
        shared_chars = shared_prefix(i,j)

        # If the mapping makes sense, then add it to the rename_dict
        if shared_chars == 10 or (shared_chars == len(i) and shared_chars == len(j)) or (shared_chars == 8 and j[8] == '_'):
            rename_dict[j] = i
            df_cols = df_cols.drop(i)
            gdf_cols = gdf_cols.drop(j)
    
    # Add to the mapping dict using unmapped values
    gdf_temp = pd.DataFrame({'strs': gdf_cols})
    gdf_temp = gdf_temp.sort_values('strs', key = lambda x:x.str.len())
    gdf_cols = pd.Index(gdf_temp['strs'].values)
    for j in gdf_cols:
        if j == 'Business_1':
            print('')
        for i in df_cols:
            if j in i:
                rename_dict[j] = i
                df_cols = df_cols.drop(i)
                break

            # If the mapping makes sense, then add it to the rename_dict
            # Checks if the shp variable name is a substring of the csv variable name
            # Or if the two strings are equal (yes, I could've coded this condition more concisely...)
            # Or if it looks like the last two chars of the shp variable name were placed there to 
            # indicate a duplicate 10 char substring and the first 8 chars are a substring of the csv variable name
            shared_chars = shared_prefix(i,j)
            if shared_chars == 10 or (shared_chars == len(i) and shared_chars == len(j)) or (shared_chars >= 8 and j[8] == '_'):
                rename_dict[j] = i
                df_cols = df_cols.drop(i)
                gdf_cols = gdf_cols.drop(j)
                break

    # Display the column mapping I wish to implement along with the shared prefix chars of the mapping
    max_col_len_gpd = max(list(map(len, rename_dict.keys())))
    max_col_len_pd = max(list(map(len, rename_dict.values())))
    spacing = (max_col_len_gpd-3) * ' '
    spacing2 = (max_col_len_pd-2) * ' '
    header = f'gpd{spacing} -> pd{spacing2} | shared_chars'
    print(header)
    print('-' * len(header))
    for k,v in rename_dict.items():
        display_j = k + (max_col_len_gpd-len(k)) * ' '
        display_i = v + (max_col_len_pd-len(v)) * ' '
        shared_chars = shared_prefix(v, k)
        print(f'{display_j} -> {display_i} | {shared_chars}')
    print('') # Newline to make the table look better 

    # Add the unused columns from the csv to the df and then print them out
    print('Unused columns from csv added to gdf:')
    for i in df_cols:
        gdf[i] = df[i]
        print(i)
    print('') # Newline to make the table look better 

    # Perform the variable name mapping
    gdf = gdf.rename(rename_dict, axis = 1)   

    # Convert NAICS column values to integers
    if 'NAICS' in gdf.columns:
        gdf['NAICS'] = gdf['NAICS'].astype('Int64')

    return gdf

def port_moody_shp():
    '''
    For processing the BC Port Moody Shapefile, copied directly from
    preprocessing.ipynb with modifications to ensure the variable 
    names are fixed
    '''

    # Define name and filepath
    name = "BC_Port_Moody_Business_Directory"
    fp = f"{raw_shp_dir}/BC_Port_Moody_shapefile/Business_Directory.shp"

    # Read in the .shp file as a geopandas dataframe
    city = gpd.read_file(fp)

    # Convert the projection to lat/lon
    print(name)
    print(city.crs)
    city = city.to_crs(epsg=4326)
    print(city.crs)

    # sub_city = city.head(500)

    # Extract the lat/lon coordinates. 
    # This is the part that appears to be different from every other .shp file
    city['lon'] = city.centroid.x
    city['lat'] = city.centroid.y

    # Fix the truncated variable names            
    city = fix_variable_names(city, f"{raw_shp_dir}/BC_Port_Moody_shapefile", name)

    # Write the dataframe to a csv file
    city.to_csv(f"{out_dir}/raw/BC_Port_Moody_Business_Directory.csv", index = False)
    print(f"File saved to {out_dir}/raw/BC_Port_Moody_Business_Directory.csv")
    city.to_csv(f"{out_dir}/processed/BC_Port_Moody_Business_Directory.csv", index = False)
    print(f"File saved to {out_dir}/processed/BC_Port_Moody_Business_Directory.csv")

def main():
    # Iterate through the ../raw/shapefiles folder
    for root, dirs, files in os.walk(raw_shp_dir):
        if 'testing' in root: # Ignore the files used for testing
            continue

        # Iterate through all files in a folder
        for file in files:
            # Only process the .shp file
            if file.endswith(".shp"):
                # Rename the file and extract the root name that is used to identify the file
                head, tail = os.path.split(os.path.join(root, file))
                head = head.replace("/home/jovyan/ODBiz/1-PreProcessing/raw/shapefiles/", '')
                head = head.replace('shapefile', '')
                head = head.replace("/", '')          
                tail = tail.replace('.shp', '')
                name = head + tail
                print(name)

                # Read in the .shp file as a geopandas dataframe
                fp = (os.path.join(root, file))
                city = gpd.read_file(fp)
                print(city.crs)

                # Convert the projection to lat/lon.
                if 'burnaby' in name.lower():
                    # This if/else statement was just for testing, 
                    # but I forgot to take it out
                    # It's probably not needed
                    city = city.to_crs(epsg=4326)
                    print('')
                else:
                    # This is needed though
                    city = city.to_crs(epsg=4326)
                print(city.crs)
                # sub_city = city.head(500)

                # Try to convert the extract lat/lon coordinates, 
                # otherwise raise an error
                try:
                    city['lon'] = city.geometry.x
                    city['lat'] = city.geometry.y
                except:
                    print('error with file above')
                    continue

                # Fix the truncated variable names
                city = fix_variable_names(city, root, name)

                # Write the dataframe to a csv file
                city.to_csv(f"{out_dir}/raw/{name}.csv", index = False)
                print(f"File saved to {out_dir}/raw/{name}.csv")
                city.to_csv(f"{out_dir}/processed/{name}.csv", index = False)
                print(f"File saved to {out_dir}/processed/{name}.csv")

    # Execute the script that fixes Port Moody's data
    port_moody_shp()

if __name__ == '__main__':
    main()