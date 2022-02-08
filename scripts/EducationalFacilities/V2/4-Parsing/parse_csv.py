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

import sys
!conda install --yes --prefix {sys.prefix} postal
import pandas as pd
from postal.parser import parse_address
import argparse

def parse_csv(df,addr_col):
    df[['street_no', 'street_name', 'LP_City', 'LP_Province', 'LP_PostCode','LP_Unit']]=df.apply(lambda x: format_parser(x[addr_col]), axis=1, result_type='expand')
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
    parser = argparse.ArgumentParser(
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
    df_out.to_csv(name_out, index=False)