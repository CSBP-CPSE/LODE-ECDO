"""
This script reads in a CSV containing an address column, and produces a version
of the csv with parsed address columns appended.
libpostal can separate into many fields, this retains only
[street number, name, postal code, city, and province]

When run directly, requires three positional arguments:

python parse_csv name_in addr_col name_out

name_in: input csv (utf-8)
addr_col: the name of the address column being parsed
name_out: the name of the output file

-Joseph Kuchar
December 14 2020
"""

"""
Quick copy-paste to run this code in terminal:

cd /home/jovyan/ODBiz/4-Parsing

python parse_csv.py input/ODBiz_Merged.csv full_address output/parsed_biz.csv

"""




import sys
import pandas as pd
from postal.parser import parse_address
from argparse import ArgumentParser
import numpy as np
from datetime import datetime as dt

def parse_csv(df, addr_col):
    df[['LP_street_no', 'LP_street_name', 'LP_City', 'LP_Province', 'LP_PostCode','LP_Unit', 
    'LP_street_no_alt'
    ]] = df.apply(lambda x: format_parser(x[addr_col]), axis=1, result_type='expand')
    return df

def format_parser(addr):

    # libpostal returns a list of tuples, this just converts it to a dictionary
    A = parse_address(addr)
    B = dict((x, y) for (y, x) in A)
    key_list = ['house_number', 'road', 'city', 'state', 'postcode', 'unit', 
                'house'
                ]
    # house = 'house'
    parsed = []
    for k in key_list:
        if k in B.keys():
            parsed.append(B[k])
        # elif (k == 'house_number') and (house in B.keys()):
        #     parsed.append(B[house])
        else:
            parsed.append('')
    return parsed

def parsing_df_wrapper(df_in: pd.DataFrame, addr_col: str):
    # Read in df and fill in na's with empty string
    start_time = dt.now()
    print(f'Begin parsing the `{addr_col}` column')
    df_in=df_in.fillna('')

    # # Remove spaces adjacent to dashes THIS CAUSES MORE PROBLEMS!!!
    # df_in[addr_col] = df_in[addr_col].str.replace(r'\s+-', '-', regex = True)
    # df_in[addr_col] = df_in[addr_col].str.replace(r'-\s+', '-', regex = True)

    # Apply Libpostal to parse address
    df_out = parse_csv(df_in, addr_col)

    # Update LP_street_no or LP_Unit with LP_street_no_alt if LP_street_no is empty string
    LP_street_no_empty = df_out['LP_street_no'] == ''
    LP_Unit_empty = df_out['LP_Unit'] == ''
    df_out.loc[~LP_street_no_empty & LP_Unit_empty, 'LP_Unit'] = df_out.loc[~LP_street_no_empty & LP_Unit_empty, 'LP_street_no_alt']
    df_out.loc[LP_street_no_empty, 'LP_street_no'] = df_out.loc[LP_street_no_empty, 'LP_street_no_alt']
    
    #street numbers that include unit number through a dash get split and put into separate columns
    # print('stop')
    split_chars = r'[\-\s]'
    df_temp = df_out.loc[df_out['LP_street_no'].str.contains(split_chars)]
    try:
        df_out[['LP2_unit', 'LP2_street_no']] = df_temp['LP_street_no'].str.split(split_chars, expand=True, regex = True)
    except:
        print('Too many dashes, spilling over parsing to extra column.')
        df_out[['LP2_unit', 'LP2_street_no', 'spill']] = df_temp['LP_street_no'].str.split(split_chars, expand=True, n=2, regex = True)
        
        # If the spillover column contains a street name, pre-pend it to LP_street_name
        has_street_name = df_out['spill'].str.contains(r'[a-z]$', na = False)
        df_out.loc[has_street_name, 'LP_street_name'] = df_out.loc[has_street_name, 'spill'] + ' ' +  df_out.loc[has_street_name, 'LP_street_name']
        
    df_out['LP2_unit'] = df_out['LP2_unit'].fillna(df_out['LP_Unit'])
    df_out['LP2_street_no'] = df_out['LP2_street_no'].fillna(df_out['LP_street_no'])

    #street numbers that include the word unit get move to new unit column and merged with other unit column
    units = df_out['LP2_street_no'].str.contains('unit', case=False)
    df_out['LP3_unit']=df_out['LP2_street_no'].where(units, np.nan)
    df_out['LP2_street_no']=df_out['LP2_street_no'].mask(units, np.nan)
    df_out['LP3_unit'] = df_out['LP3_unit'].fillna(df_out['LP2_unit'])
    
    #df2_temp = df_out.loc[df_out['LP2_street_no'].str.contains(" ", na)]    
    #print(df_temp)
    #df_out[['LP3_unit', 'LP3_street_no']] = df2_temp['LP2_street_no'].str.split(' ', expand=True)
    #df_out['LP3_unit'] = df_out['LP3_unit'].fillna(df_out['LP2_Unit'])
    #df_out['LP3_street_no'] = df_out['LP3_street_no'].fillna(df_out['LP2_street_no'])    
    
    exetime = dt.now() - start_time
    print(f'Execution finished in {exetime.total_seconds()} seconds')

    return df_out

def parsing_file_wrapper(name_in: str, addr_col: str, name_out: str):
    df_in = pd.read_csv(name_in, dtype='str', low_memory=False)
    print(f'File {name_in} loaded')
    df_out = parsing_df_wrapper(df_in, addr_col)

    print(f'df has been parsed! Saving file to {name_out}')
    df_out.to_csv(name_out, index=False)
    print(f'File saved to {name_out}')

def main():

    # parser = ArgumentParser(
    #     description='Apply libpostal address parser to an address column in a csv')
    # parser.add_argument('name_in',
    #                     help='Name/Path of input file')
    # parser.add_argument('addr_col',
    #                     help='Name of address column to pass to parser')
    # parser.add_argument('name_out',
    #                     help='Name/Path of output file')
    # args = parser.parse_args()

    # name_in = args.name_in
    # addr_col = args.addr_col
    # name_out = args.name_out

    name_in = '/home/jovyan/ODBiz/4-Parsing/input/ODBiz_Merged.csv' 
    addr_col = 'full_address' 
    name_out = '/home/jovyan/ODBiz/4-Parsing/output/parsed_biz.csv'

    parsing_file_wrapper(name_in, addr_col, name_out)
    
if __name__ == "__main__":
    main()


