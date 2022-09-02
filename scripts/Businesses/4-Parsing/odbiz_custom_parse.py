import pandas as pd 
from tqdm import tqdm
import numpy as np
from parse_csv import parsing_df_wrapper

def duplicate_dashes(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Replace dashes to avoid Excel's date conversion
    '''
    new_df = df.copy()

    new_df['LP2_unit'] = new_df['LP2_unit'].str.replace('-', '--')
    new_df['LP_street_no'] = new_df['LP_street_no'].str.replace('-', '--')
    
    return new_df

def save_df_to_csv(df, output_path: str, **kwargs):
    '''
    Saves df to_csv and prints a confirmation message

    Arguments:
        - df (pd.DataFrame): The main dataframe being parsed
        - **kwargs: Optional keyword arguments to pass along to panda's df.to_csv() function
        
    Side Effects:
        - Outputs df as a csv
    '''

    df.to_csv(output_path, **kwargs)
    print(f'df saved to {output_path}')

def simple_parse(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    '''
    Split LP_street_no by dashes (-), set the right most value as LP2_street_no, 
    set everything else as LP2_unit
    
    Arguments:
        - df (pd.DataFrame): The main dataframe being parsed
        - output_path (str): Path of the csv file to output the results of this parsing
        
    Side Effects:
        - Outputs df as a csv
    '''

    new_df = df.copy()

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

    # Set right most value as street_no, everything else is unit
    temp = new_df.loc[localfiles_idx, 'LP_street_no'].str.rsplit('-', expand = True, n = 1)
    new_df.loc[localfiles_idx, ['LP2_unit', 'LP2_street_no']] = temp.rename(columns = {0: 'LP2_unit', 1: 'LP2_street_no'})

    new_df.to_csv(output_path, index = False)
    print(f'Saved new_df to {output_path}')

    return new_df


def toronto_parse(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    '''
    Apply a parsing rule specific to several Toronto businesses

    Arguments:
        - df (pd.DataFrame): The main dataframe being parsed
        - output_path (str): Path of the csv file to output the results of this parsing
        
    Side Effects:
        - Outputs df as a csv
    '''

    new_df = df.copy()

    ### Apply Toronto's modified parsing rule
    localfiles_idx = new_df['localfile'] == 'ON_Toronto_Business_Licences.csv'
    has_comma = new_df['full_address'].str.contains(',') & localfiles_idx

    # If there's no comma, set right most value as street_no, everything else is unit
    new_df.loc[~has_comma, ['LP2_unit', 'LP2_street_no']] = new_df.loc[~has_comma, 'LP_street_no'].str.rsplit('-', expand = True, n = 1).rename(columns = {0: 'LP2_unit', 1: 'LP2_street_no'})

    # If there is a comma, apply parsing rule
    new_df.loc[has_comma, ['LP2_street_no', 'LP2_unit']] = new_df.loc[has_comma, 'full_address'].str.extract(r'(\d+)[A-Z\s]*,\s?(.*)').rename(columns = {0: 'LP2_street_no', 1: 'LP2_unit'})

    new_df.to_csv(output_path, index = False)
    print(f'Saved new_df to {output_path}')

    return new_df


def flag_incorrect_QC(df: pd.DataFrame, QC_parsed_wrong_df_path: str) -> pd.DataFrame:
    '''
    Identify incorrectly parsed entries in the QC dataset and flag them
    by setting LP2_unit and LP2_street_no as nan
    
    Arguments:
        - df (pd.DataFrame): The main dataframe being parsed
        - QC_parsed_wrong_df_path (str): Path of the csv file to output the results of this parsing
    '''
    df = df.copy()

    ### Identify QC entries with the most common pattern, flag them!
    QC_df = pd.read_csv(QC_parsed_wrong_df_path, dtype = str)
    common_pats = [
        "<unit>-<street_no> <street_name>",
        "<unit>-<street_no>, <street_name>",
        "<unit>-<street_no> , <street_name>"
    ]
    QC_wrong_idxs = QC_df.loc[~QC_df['pattern'].isin(common_pats), 'idx']           
    df.loc[QC_wrong_idxs, ['LP2_unit', 'LP2_street_no']] = np.nan

    return df

def detect_street_no_1st(df: pd.DataFrame) -> pd.Index:
    '''
    Detects if first number in sequence separated by dashes is the street_no

    Returns:
        A pandas Index of boolean values
    '''

    df = df.copy()

    st_no_1st_df = df[['LP_street_no']].copy()
    temp = st_no_1st_df['LP_street_no'].str.split('-', expand = True)
    second_col_contains_letter = temp[1].str.contains(r'\D', na = False)
    for col in tqdm(temp.columns, desc = 'Determining if 1st number in dashes sequence is the max'):
        temp[col] = pd.to_numeric(temp[col], errors = 'coerce', downcast = 'integer')
        temp[col] = np.floor(temp[col]).astype(pd.Int64Dtype())

    print('Calculating max col indicies')
    temp['max_col'] = temp.max(axis = 1).astype(pd.Int64Dtype())
    temp['first_col_max'] = (~temp[2].isna()) & (temp['max_col'] == temp[0])

    st_no_1st_df = st_no_1st_df.join(temp)
    st_no_1st_df['has_dash_and_1st_col_max'] = st_no_1st_df['LP_street_no'].str.contains('-') & st_no_1st_df['first_col_max']
    has_dash_and_1st_col_max = st_no_1st_df['has_dash_and_1st_col_max'].fillna(False) | second_col_contains_letter

    return has_dash_and_1st_col_max


def detect_blank_street_no(df: pd.DataFrame) -> pd.Index:
    '''
    Detects if absolutely no street_no info has been parsed

    Returns:
        A pandas Index of boolean values
    '''

    df = df.copy()
    street_no_conds = [
            (df['full_address'].str.contains(r'\d')),   # full_address contains a digit
            (df['street_no'].isna()),                   # street_no is blank
            (df['LP_street_no'].isna()),                # LP_street_no is blank
            (df['LP2_street_no'].isna()),               # LP2_street_no is blank
            ]
    street_no_blank = True
    for i in street_no_conds:
        street_no_blank = street_no_blank & i

    return street_no_blank

def detect_unit_starts_non_digit(df: pd.DataFrame, regex_search: str) -> pd.Index:
    '''
    Detects if unit starts with a non-digit character

    Arguments:
        - df (pd.DataFrame): The main dataframe being parsed
        - regex_search (str): A regex string to use in the search function

    Returns:
        A pandas Index of boolean values
    '''

    df = df.copy()
    unit_starts_non_digit = df['full_address'].str.contains(regex_search, na = False)
    return unit_starts_non_digit

def detect_blank_street_names(df: pd.DataFrame, OUT_OF_TOWN_VARS_LIST: list) -> pd.Index:
    '''
    Detects if LP_street_name is blank given non blank full addresses that aren't "out of town"

    Arguments:
        - df (pd.DataFrame): The main dataframe being parsed
        - OUT_OF_TOWN_VARS_LIST (list): A list of full address values that should be discarded due to not providing enough info

    Returns:
        A pandas Index of boolean values
    '''

    new_df = df.copy()
    blank_street_names = new_df['full_address'].notnull() & new_df['LP_street_name'].isnull() & ~(new_df['LP_street_name'].isin(OUT_OF_TOWN_VARS_LIST))
    return blank_street_names

def fix_postcode_errs(parsing_errs_df: pd.DataFrame, usa_postcode_err: pd.Series, postal_code_csv: str = None) -> pd.DataFrame:
    '''
    Fixes postal code errors

    Arguments:
        - parsing_errs_df (pd.DataFrame): A subset of the main dataframe containing only detected parsing errors.
        - usa_postcode_err (pd.Series): A boolean series that indicates which entries has the usa postal code error
        - postal_code_csv (str): Default = None. The file path to output the results of this parsing

    Side Effects:
        - Outputs usa_postcode_err_df as a csv
    '''
    # For these entries, LP parsed the street no as a postal code, and the unit no as a street no. 
    # This block of code maps the values to their proper column
    usa_postcode_err_df = parsing_errs_df.loc[usa_postcode_err].copy()
    usa_postcode_err_df = usa_postcode_err_df.fillna('')
    usa_postcode_err_df['LP2_unit'] = (usa_postcode_err_df['LP2_unit'] + ' ' + usa_postcode_err_df['LP2_street_no']).str.lstrip()
    usa_postcode_err_df['LP2_street_no'] = usa_postcode_err_df['LP_PostCode']
    usa_postcode_err_df['LP_PostCode'] = ''
    usa_postcode_err_df = usa_postcode_err_df.replace('', np.nan)

    # Save to csv
    if postal_code_csv is not None:
        save_df_to_csv(usa_postcode_err_df, postal_code_csv, index = True)

    return usa_postcode_err_df

def extract_parsing_errs(df: pd.DataFrame, err_idxs_dict: dict, OUT_OF_TOWN_VARS_LIST: list, main_df_output_path: str, parsing_errs_output_path: str) -> pd.DataFrame:
    '''
    Extracts all the entries with parsing errors from the main df by applying inclusive OR to 
    all Index objects stored in err_idxs_dict. 

    Side Effects:
        - Adds 2 columns to df, a boolean that indicates whether the entry has a parsing error 
        and a column with a brief description of the errors
        - Saves two dfs to file, the main df and the extraction of all detected parsing errors

    Arguments:
        - df: The main dataframe
        - err_idxs_dict: A dictionary of pandas Index of boolean values to indicate which entries have 
        a parsing error
        - OUT_OF_TOWN_VARS_LIST: A list of full address values that should be discarded due to not providing enough info
        - main_df_output_path: File path to save the main df
        - parsing_errs_output_path: File path to save the parsing errors df

    Returns:
        - parsing_errs_df: A dataframe of the extracted entries with parsing errors
    '''
    
    # Extract the indicies of all entries with detected parsing errors
    err_idxs = False
    for v in err_idxs_dict.values():
        err_idxs = err_idxs | v

    parsing_errs_df = df.loc[err_idxs].copy()
    parsing_errs_df = parsing_errs_df.loc[~(parsing_errs_df['full_address'].isin(OUT_OF_TOWN_VARS_LIST))]

    # Check for already parsed data from source and remove them
    source_parsed = (parsing_errs_df['street_name'].notnull()) & (~err_idxs_dict['invalid_street_no']) # & (parsing_errs_df['street_no'].notnull())
    parsing_errs_df = parsing_errs_df[~source_parsed]
    df['parsing_err_exists'] = False
    df.loc[parsing_errs_df.index, 'parsing_err_exists'] = True
    parsing_errs_df.loc[:,'parsing_err_exists'] = True

    # Add descriptions of the parsing error
    parsing_errs_df['parsing_err'] = ''
    for k, v in err_idxs_dict.items():
        parsing_errs_df.loc[v, 'parsing_err'] = parsing_errs_df.loc[v, 'parsing_err'] + (k + ',')

    print(f'There are {parsing_errs_df.shape[0]} rows of incorrectly parsed addresses')

    # Save the dfs to csv
    save_df_to_csv(parsing_errs_df, parsing_errs_output_path, index = True)
    save_df_to_csv(df, main_df_output_path, index = True)

    return parsing_errs_df

def fix_dashes_with_spaces(parsing_errs_df: pd.DataFrame, dashes_with_spaces_path: str, ORDINAL_NUMBER_DETECTION: str, CAD_POSTCODE_FORMAT: str) -> pd.DataFrame:
    '''
    Fixes entries where spaces adjacent to dashes causes parsing errors

    Arguments:
        - parsing_errs_df (pd.DataFrame): A dataframe of the extracted entries with parsing errors
        - dashes_with_spaces_path (str): The file path used to save the results of this parsing
        - ORDINAL_NUMBER_DETECTION (str): A regex string used to detect ordinal numbers in addressses
        - CAD_POSTCODE_FORMAT (str): A regex string used to detect valid Canadian postal codes
    
    Returns:
        - dashes_with_spaces_df: A dataframe with some of the dashes_with_spaces errors fixed

    Side Effects:
        - Calls fix_postcode_errs()
        - Saves parsing_errs_df to dashes_with_spaces_path as a csv
    '''

    # DEBUG_COLS = ['full_address', 'LP2_unit', 'LP2_street_no', 'LP_street_name']

    # Remove whitespaces, then feed through libpostal again
    dashes_with_spaces_df = parsing_errs_df[parsing_errs_df['parsing_err'] == 'dashes_with_spaces,'].copy()
    full_address_alt = 'full_address_alt'
    dashes_with_spaces_df[full_address_alt] = dashes_with_spaces_df['full_address'].str.replace(r'\s*-\s*', '-', regex = True, n = 1)
    dashes_with_spaces_df = parsing_df_wrapper(dashes_with_spaces_df, full_address_alt)

    # Mark everything as parsed, then mark detected anomolies as not parsed
    dashes_with_spaces_df['parsing_err_exists'] = True 
    dws_parsing_errs = [
        dashes_with_spaces_df['LP2_street_no'].str.contains(r'\D', regex = True), # LP2_street_no contains non-digit chars
        dashes_with_spaces_df['full_address'].str.contains(',') & (dashes_with_spaces_df['LP2_unit'].str.fullmatch('') | dashes_with_spaces_df['LP2_street_no'].str.fullmatch('')), # full_addr contains comma and one of unit or street_no is empty
        dashes_with_spaces_df['LP2_street_no'].str.fullmatch(''),
        dashes_with_spaces_df['LP_street_name'].str.fullmatch(''),
        dashes_with_spaces_df['LP2_street_no'] == '1',
        dashes_with_spaces_df['LP2_street_no'] == '10',
        dashes_with_spaces_df['full_address'].str.contains(r'\d\s*(?:avenue|street)', case = False, regex = True) & ~(dashes_with_spaces_df['full_address'].str.contains(ORDINAL_NUMBER_DETECTION, case = False, regex = True)),
        dashes_with_spaces_df['full_address'].str.contains(r'^[A-z]{2,}', case = False, regex = True),
    ]
    parsing_err_idxs = False
    for i in dws_parsing_errs:
        parsing_err_idxs = parsing_err_idxs | i
    dashes_with_spaces_df.loc[~parsing_err_idxs, 'parsing_err_exists'] = False

    # Sometimes, the original parsing was better than without the space
    df2 = dashes_with_spaces_df.loc[dashes_with_spaces_df['parsing_err_exists']].copy()
    df2 = parsing_df_wrapper(df2, 'full_address')
    dashes_with_spaces_df.update(df2)

    # # Fix the new postal code errors that pop up
    # usa_postcode_err = dashes_with_spaces_df['LP_PostCode'].str.fullmatch(r'\d+', na = False)
    # usa_postcode_err = fix_postcode_errs(dashes_with_spaces_df, usa_postcode_err)

    # LP_street_name contains two numbers seperated by a space
    two_nums_with_space_regex = r'^(\d+)\s+(\d+.*)'
    two_nums_with_space_bool = dashes_with_spaces_df['LP_street_name'].str.contains(two_nums_with_space_regex, na = False, regex = True)
    two_nums_with_space_df = dashes_with_spaces_df['LP_street_name'].str.extract(two_nums_with_space_regex, expand = True)
    dashes_with_spaces_df.loc[two_nums_with_space_bool, 'LP2_unit'] = dashes_with_spaces_df.loc[two_nums_with_space_bool, 'LP2_unit'] + dashes_with_spaces_df.loc[two_nums_with_space_bool, 'LP2_street_no']
    dashes_with_spaces_df.loc[two_nums_with_space_bool, 'LP2_street_no'] = two_nums_with_space_df.loc[two_nums_with_space_bool, 0]
    dashes_with_spaces_df.loc[two_nums_with_space_bool, 'LP_street_name'] = two_nums_with_space_df.loc[two_nums_with_space_bool, 1]

    return dashes_with_spaces_df

def main():
    # Define filepaths
    input_csv_path = '/home/jovyan/ODBiz/4-Parsing/output/parsed_biz.csv'
    df2_path = '/home/jovyan/ODBiz/4-Parsing/double_check/parsed_with_easy_blanket_rule.csv'
    dfTO_path = '/home/jovyan/ODBiz/4-Parsing/double_check/parsed_with_spillover_toronto.csv'
    QC_parsed_wrong_df_path = '/home/jovyan/ODBiz/4-Parsing/custom_parsing_data/QC_Biz_parsed_wrong.csv'
    postal_code_df_path = '/home/jovyan/ODBiz/4-Parsing/custom_parsing_data/postal_code_err.csv'
    dashes_with_spaces_path = '/home/jovyan/ODBiz/4-Parsing/custom_parsing_data/dashes_with_space.csv'
    main_df_output_path = '/home/jovyan/ODBiz/4-Parsing/custom_parsing_data/main_with_detected_parsing_errors.csv'
    parsing_errs_output_path = '/home/jovyan/ODBiz/4-Parsing/custom_parsing_data/extract_detected_parsing_errors.csv'
    output_csv_path = '/home/jovyan/ODBiz/4-Parsing/output/2-parsed_biz.csv'
    
    # Define some useful variables
    OUT_OF_TOWN_VARS_LIST = [ # All entries where full_address was a full match with one of the values in this list were removed
        '-',                                  
        'BUSINESS - OUT OF TOWN SQUAMISH',    
        'BUSINESS - OUT OF TOWN',             
        'NON-RESIDENT',                       
        'BUSINESS-NON RESIDENT'             
    ]
    ORDINAL_NUMBER_DETECTION = r'1st |2nd |3rd |\dth '
    # DEBUG_COLS = ['full_address', 'LP2_unit', 'LP2_street_no', 'LP_street_name']
    CAD_POSTCODE_FORMAT = r'[A-z]\d[A-z]\s*\d[A-z]\d'

    # Load the csv
    total_lines = 803584
    chunksize = 10000
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(input_csv_path,
                                            chunksize=chunksize, 
                                            dtype=str), 
                                        desc='Loading data', 
                                        total=total_lines//chunksize+1)
                    ])
    # df = pd.read_csv(input_csv, dtype=str)
    df = df.set_index('idx') # This line of code is causing the code to halt without error messages. But it is necessary for the rest of the program :(
    num_of_rows = df.shape[0]
    print(f'Successfully loaded {input_csv_path}')
    print(f'df has {num_of_rows} rows')

    # Extract only entries that spillover their unit+street_no values
    new_df = df[~df['spill'].isna()].copy()
    new_df = new_df[['localfile', 'business_name', 'full_address', 'LP2_unit', 'LP2_street_no', 'spill', 'LP_street_no', 'LP_street_name', 'LP_City', 'LP_Province', 'LP_PostCode', 'LP_Unit', 'LP3_unit']]

    # Apply a simple parsing rule
    print('Applying simple_parse')
    new_df = simple_parse(new_df, df2_path)

    # Apply a parsing rule specific to Toronto businesses
    print('Applying toronto_parse')
    new_df = toronto_parse(new_df, dfTO_path)

    # Update main df with changes so far
    print('Merging above changes with main df')
    # new_df = new_df.set_index('idx')
    df.update(new_df) 

    # Flag incorrectly parsed QC entries
    df = flag_incorrect_QC(df, QC_parsed_wrong_df_path)

    ### Create df of incorrectly parsed addresses (for entries with full_address)

    # Detect if first number in sequence separated by dashes is the street_no
    has_dash_and_1st_col_max = detect_street_no_1st(df)

    # Detect values incorrectly parsed as postal codes
    usa_postcode_err = df['LP_PostCode'].str.fullmatch(r'\d+', na = False)

    # Detect dashes with spaces, libpostal freaks out when it encounters these
    dashes_with_spaces = df['full_address'].str.contains(r'\s+-|-\s+', na = False) & ~(df['LP_street_name'].str.contains(ORDINAL_NUMBER_DETECTION, regex = True) & ((~(df['LP2_unit'].isnull()) | ~(df['LP2_street_no'].str.contains(r'\s', regex = True, na = False))))) & (~(df['full_address'].str.startswith('#', na = False)))

    # Detect if absolutely no street_no info has been parsed
    street_no_blank = detect_blank_street_no(df)

    # Detect if first value is a unit separated by a dash, and starts with a non-digit character
    unit_regex_group = r'^([^\d\s]+[A-z\d\.#\/]+)\s*-\s*([A-z\d\.#\/]+)\s*'
    unit_starts_non_digit = detect_unit_starts_non_digit(df, unit_regex_group)

    # Detect blank street names
    blank_street_names = detect_blank_street_names(df, OUT_OF_TOWN_VARS_LIST)

    # Detect invalid street_no
    invalid_street_no = df['street_no'].str.contains(r'[\D\s]', regex = True, na = False)

    # Extract only detected patterns
    err_idxs_dict = {# All values should be of pd.Index where all indicies are the same as df.index!
                    'street_no_blank': street_no_blank,
                    'usa_postcode_err': usa_postcode_err,
                    'dashes_with_spaces': dashes_with_spaces,
                    'has_dash_and_1st_col_max': has_dash_and_1st_col_max,
                    'unit_starts_non_digit': unit_starts_non_digit,
                    'blank_street_names': blank_street_names,
                    'invalid_street_no': invalid_street_no,
                    # 'street_name_in_city': street_name_in_city
    }
    parsing_errs_df = extract_parsing_errs(df, err_idxs_dict, OUT_OF_TOWN_VARS_LIST, main_df_output_path, parsing_errs_output_path)

    # Fix usa postal code error
    usa_postcode_err_df = fix_postcode_errs(parsing_errs_df, usa_postcode_err, postal_code_df_path)
    print('Updating the big parsed csv with postal code error correction...')
    df.update(usa_postcode_err_df)    
    parsing_errs_df.update(usa_postcode_err_df)    

    # Fix dashes with space error
    dashes_with_spaces_df = fix_dashes_with_spaces(parsing_errs_df, dashes_with_spaces_path, ORDINAL_NUMBER_DETECTION, CAD_POSTCODE_FORMAT)
    df.update(dashes_with_spaces_df)    
    parsing_errs_df.update(dashes_with_spaces_df)   

    # Add a column to indicate whether an entry was flagged as a parsing error
    df['flagged_parsing_err'] = False
    df.loc[parsing_errs_df.index, 'flagged_parsing_err'] = True

    ### For the addresses that I know are parsed from the parsing_errs_df, mark them as parsed (parsing_err_exists == False)
    fixed_conds = [
                parsing_errs_df['parsing_err'] == 'usa_postcode_err,', # Only postal codes caused the error
                # parsing_errs_df['parsing_err'] == 'dashes_with_spaces,', # Only dashes with spaces caused the error
                parsing_errs_df['localfile'] == 'BC_Victoria_Business_Licences.csv', # Victoria was determined to be fully parsed 
                unit_starts_non_digit & (~parsing_errs_df['LP2_unit'].isna()) & (~(parsing_errs_df['LP2_street_no'].str.contains(r'[\D\s]', na = False))), # New iteration of parse_csv fixed most of the units starting with non-digits
                parsing_errs_df['LP_street_name'].str.contains(r'^\d*\s(?:st$|street$|ave)', na = False, regex = True), # if the street name is "num avenue" or "num street" formatted in a particular way, these ones were parsed correctly
                ]
    fixed_conds_idxs = False 
    for i in fixed_conds:
        fixed_conds_idxs = fixed_conds_idxs | i
    fixed_conds_idxs = fixed_conds_idxs & (~parsing_errs_df['LP_street_name'].isna())
    parsed_idxs = parsing_errs_df[fixed_conds_idxs].index
    parsing_errs_df.loc[parsed_idxs, 'parsing_err_exists'] = False
    print(f'Total    {parsing_errs_df.shape[0]}')
    print('parsing_errs_df[parsing_err_exists].value_counts():')
    parsing_val_counts = parsing_errs_df['parsing_err_exists'].value_counts()
    print(parsing_val_counts)
    print(f'Success percentage = {np.floor(100 * parsing_val_counts[False] / parsing_errs_df.shape[0])} %')
    print('Remaining parsing required (breakdown):')
    print(parsing_errs_df.loc[parsing_errs_df['parsing_err_exists'],'parsing_err'].value_counts())

    ### Apply a custom regex parser for units that start with a letter (This doesn't actually work properly so I didn't keep these results in the final, but removing only this block of code may break other things)
    re_mapping = {
                    0: 'regex_g1', 
                    1: 'regex_g2'
                    }
    temp = parsing_errs_df['full_address'].str.extract(unit_regex_group)
    parsing_errs_df[['regex_g1', 'regex_g2']] = temp.rename(columns = re_mapping)
    for i in re_mapping.values():
        parsing_errs_df[i] = parsing_errs_df[i].str.lower()

    # Reorder parsing_errs_df for easier debugging
    parsing_errs_df['idx'] = parsing_errs_df.index
    column_reorder = [
                                        'full_address',
                                        'LP_street_name',
                                        'idx',
                                        'postal_code',
                                        'unit',
                                        'street_no',
                                        'street_name',
                                        'LP_Unit',
                                        'LP_street_no',
                                        'LP_City',
                                        'LP_Province',
                                        'LP_PostCode',
                                        'LP_street_no_alt',
                                        'LP2_unit',
                                        'LP2_street_no',
                                        'spill',
                                        'LP3_unit',
                                        'regex_g1',
                                        'regex_g2',
                                        'parsing_err_exists',
                                        'parsing_err',
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
                                        'NAICS_descr2',
                                        'alt_econ_act_code',
                                        'alt_econ_act_descrip',
                                        'latitude',
                                        'longitude',
                                        'full_address_2',
                                        'mailing_address',
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
                                        ]
    len_column_reorder = len(column_reorder)
    parsing_errs_cols = parsing_errs_df.shape[1]
    if len_column_reorder != parsing_errs_cols:
        print('WARNING! There might be some missing columns!')
        print(f'len_column_reorder = {len_column_reorder}')
        print(f'parsing_errs_cols = {parsing_errs_cols}')
    parsing_errs_df = parsing_errs_df[column_reorder]

    # Save parsing_errs_df
    save_df_to_csv(parsing_errs_df, parsing_errs_output_path, index = False)
  
    # Save the main csv
    df.to_csv(output_csv_path, index = True)
    print(f'Saved df to {output_csv_path}')

if __name__ == '__main__':
    main()