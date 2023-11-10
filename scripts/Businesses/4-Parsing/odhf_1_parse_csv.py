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

cd /home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/4-Parsing

python parse_csv.py merged.csv street_addr parsed.csv
python 1-parse_csv.py test_odbiz_merge.csv full_address parsed_biz.csv
python odhf_1_parse_csv.py input/ODBiz_Merged.csv full_address output/parsed_biz.csv

"""




import sys
import pandas as pd
from postal.parser import parse_address
from argparse import ArgumentParser
import numpy as np

def parse_csv(df, addr_col):
    df[['LP_street_no', 'LP_street_name', 'LP_City', 'LP_Province', 'LP_PostCode','LP_Unit']] = df.apply(lambda x: format_parser(x[addr_col]), axis=1, result_type='expand')
    return df

def format_parser(add):

    # libpostal returns a list of tuples, this just converts it to a dictionary
    A = parse_address(add)
    B = dict((x, y) for (y, x) in A)
    key_list = ['house_number', 'road', 'city', 'state', 'postcode', 'unit']
    parsed = []
    for k in key_list:
        if k in B.keys():
            parsed.append(B[k])
        else:
            parsed.append('')
    return parsed

if __name__ == "__main__":
    parser = ArgumentParser(
        description='Apply libpostal address parser to an address column in a csv')
    parser.add_argument('name_in',
                        help='Name/Path of input file')
    parser.add_argument('addr_col',
                        help='Name of address column to pass to parser')
    parser.add_argument('name_out',
                        help='Name/Path of output file')
    args = parser.parse_args()

    name_in = args.name_in
    addr_col = args.addr_col
    name_out = args.name_out
    df_in = pd.read_csv(name_in, dtype='str', low_memory=False)
    df_in=df_in.fillna('')
    df_out = parse_csv(df_in, addr_col)
    
#street numbers that include unit number through a dash get split and put into separate columns
    df_temp = df_out.loc[df_out['LP_street_no'].str.contains("-")]
    df_out[['LP2_unit', 'LP2_street_no']] = df_temp['LP_street_no'].str.split('-', expand=True)
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
    
    df_out.to_csv(name_out, index=False)
    
    


