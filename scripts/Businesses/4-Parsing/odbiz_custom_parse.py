import pandas as pd 
from tqdm import tqdm
import numpy as np



def main():
    # Define filepaths
    input_csv = '/home/jovyan/ODBiz/4-Parsing/output/parsed_biz.csv'
    new_df_path = '/home/jovyan/ODBiz/4-Parsing/double_check/parsed_with_spillover.csv'
    df2_path = '/home/jovyan/ODBiz/4-Parsing/double_check/parsed_with_easy_blanket_rule.csv'
    dfTO_path = '/home/jovyan/ODBiz/4-Parsing/double_check/parsed_with_spillover_toronto.csv'
    QC_parsed_wrong_df_path = '/home/jovyan/ODBiz/4-Parsing/custom_parsing_data/QC_Biz_parsed_wrong.csv'
    output_csv = '/home/jovyan/ODBiz/4-Parsing/output/2-parsed_biz.csv'
    unparsed_addrs_path = '/home/jovyan/ODBiz/4-Parsing/custom_parsing_data/unparsed_addresses.csv'
    
    # Load the csv
    total_lines = 803658
    chunksize = 10000
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(input_csv,
                                            chunksize=chunksize, 
                                            dtype=str), 
                                        desc='Loading data', 
                                        total=total_lines//chunksize+1)
                    ])
    num_of_rows = df.shape[0]
    print(f'Successfully loaded {input_csv}')
    print(f'df has {num_of_rows} rows')

    # Extract only entries that spillover their unit+street_no values
    new_df = df[~df['spill'].isna()].copy()
    new_df = new_df[['idx', 'localfile', 'business_name', 'full_address', 'LP2_unit', 'LP2_street_no', 'spill', 'LP_street_no', 'LP_street_name', 'LP_City', 'LP_Province', 'LP_PostCode', 'LP_Unit', 'LP3_unit']]
    new_df.to_csv(new_df_path, index = False)
    print(f'Saved new_df to {new_df_path}')


    ### Apply the easiest blanket rule on the specific datasets below
    localfiles = [  'BC_Victoria_Business_Licences.csv',
                    # 'BC_Indigenous_Business_Listings.csv',
                    'BC_Chilliwack_Business_Licences.csv',
                    'ON_Brampton_Business_Directory.csv',
                    'QC_Etablissements.csv',
                    # 'ON_Toronto_Business_Licences.csv',
                    # 'Indigenous_Business_Directory.csv',
                    ]
    localfiles_idx = new_df['localfile'].isin(localfiles)
    # df2 = new_df.copy()

    # Set right most value as street_no, everything else is unit
    temp = new_df.loc[localfiles_idx, 'LP_street_no'].str.rsplit('-', expand = True, n = 1)
    new_df.loc[localfiles_idx, ['LP2_unit', 'LP2_street_no']] = temp.rename(columns = {0: 'LP2_unit', 1: 'LP2_street_no'})

    # # Replace dashes to avoid Excel's date conversion
    # new_df.loc[localfiles_idx, 'LP2_unit'] = new_df.loc[localfiles_idx, 'LP2_unit'].str.replace('-', '--')
    # new_df.loc[localfiles_idx, 'LP_street_no'] = new_df.loc[localfiles_idx, 'LP_street_no'].str.replace('-', '--')

    new_df.to_csv(df2_path, index = False)
    print(f'Saved new_df to {df2_path}')


    ### Apply Toronto's modified parsing rule
    localfiles = [  
                    # 'BC_Victoria_Business_Licences.csv',
                    # 'BC_Indigenous_Business_Listings.csv',
                    # 'BC_Chilliwack_Business_Licences.csv',
                    # 'ON_Brampton_Business_Directory.csv',
                    # 'QC_Etablissements.csv',
                    'ON_Toronto_Business_Licences.csv',
                    # 'Indigenous_Business_Directory.csv',
                    ]
    localfiles_idx = new_df['localfile'] == 'ON_Toronto_Business_Licences.csv'
    has_comma = new_df['full_address'].str.contains(',') & localfiles_idx

    # If there's no comma, set right most value as street_no, everything else is unit
    new_df.loc[~has_comma, ['LP2_unit', 'LP2_street_no']] = new_df.loc[~has_comma, 'LP_street_no'].str.rsplit('-', expand = True, n = 1).rename(columns = {0: 'LP2_unit', 1: 'LP2_street_no'})

    # If there is a comma, apply parsing rule
    new_df.loc[has_comma, ['LP2_street_no', 'LP2_unit']] = new_df.loc[has_comma, 'full_address'].str.extract('(\d+)[A-Z\s]*,\s?(.*)').rename(columns = {0: 'LP2_street_no', 1: 'LP2_unit'})

    # # Replace dashes to avoid Excel's date conversion
    # new_df['LP2_unit'] = new_df['LP2_unit'].str.replace('-', '--')
    # new_df['LP_street_no'] = new_df['LP_street_no'].str.replace('-', '--')

    new_df.to_csv(dfTO_path, index = False)
    print(f'Saved new_df to {dfTO_path}')


    ### Identify QC entries with the most common pattern, flag them!
    QC_df = pd.read_csv(QC_parsed_wrong_df_path, dtype = str)
    common_pats = [
        "<unit>-<street_no> <street_name>",
        "<unit>-<street_no>, <street_name>",
        "<unit>-<street_no> , <street_name>"
    ]
    QC_wrong_idxs = QC_df.loc[~QC_df['pattern'].isin(common_pats), 'idx']
    new_df = new_df.set_index('idx')
    
    df = df.set_index('idx')
    print('Updating the big parsed csv...')
    df.update(new_df)    
    df.loc[QC_wrong_idxs, ['LP2_unit', 'LP2_street_no']] = np.nan
    df.to_csv(output_csv, index = True)
    print(f'Saved new_df to {output_csv}')
    # print(f'Reminder: df was not saved!')

    ### Create df of incorrectly parsed addresses (for entries with full_address)
    street_no_conds = [
            (df['full_address'].str.contains(r'\d')),   # full_address contains a digit
            (df['street_no'].isna()),                   # street_no is blank
            (df['LP_street_no'].isna()),                # LP_street_no is blank
            (df['LP2_street_no'].isna()),               # LP2_street_no is blank
            ]
    usa_postcode_err = df['LP_PostCode'].str.fullmatch(r'\d+', na = False)
    dashes_with_spaces = df['full_address'].str.contains(r'\s+-\s?|\s?-\s+', na = False)
    street_no_blank = True
    for i in street_no_conds:
        street_no_blank = street_no_blank & i
    idxs = street_no_blank | usa_postcode_err | dashes_with_spaces
    unparsed_df = df.loc[idxs].copy()
    unparsed_df['parsing_err'] = ''
    unparsed_df.loc[street_no_blank, 'parsing_err'] = unparsed_df.loc[street_no_blank, 'parsing_err'] + 'street_no_blank,'
    unparsed_df.loc[usa_postcode_err, 'parsing_err'] = unparsed_df.loc[usa_postcode_err, 'parsing_err'] + 'usa_postcode_err,'
    unparsed_df.loc[dashes_with_spaces, 'parsing_err'] = unparsed_df.loc[dashes_with_spaces, 'parsing_err'] + 'dashes_with_spaces,'

    # unparsed_df.to_csv(unparsed_addrs_path, index = True)
    # print(f'Saved unparsed_df to {unparsed_addrs_path}')
    print(f'There are {unparsed_df.shape[0]} rows of incorrectly parsed addresses')


    ### Unit starts with letter
    re_pat = r'^[\dA-z#0-9]*\s*-\s*[\dA-z#0-9]*'
    

    print('')

if __name__ == '__main__':
    main()