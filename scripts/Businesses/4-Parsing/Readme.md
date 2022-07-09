# What is the goal of parsing in the project?
We have different formats for addresses. If you take a look at the merged.csv file, you will notice that some addresses are all together under the full_address column, while some addresses are split into street_no, street_name, postal_code, etc. 

The objective is to split the addresses that are NOT split (which is the majority), and make a individual columns for street number and name, unit number, city and postal code

# parse_csv.py
This python script's purpose is to to separate the full addresses thanks to the pypostal library. New columns (LP_...) are created with the parsed addresses, WITHOUT including the addresses that were already split. The output of this file is parsed.csv. 

There exists an issue with the LP_street_no column: sometimes, full addresses will have unit number and street number separated with a dash (12-235, for example). The parsing code recognizes this as a full street number, instead of 2 different values, which is why we split these wherever necessary. This is why there are two additional columns in the parsed file: LP2_unit and LP2_street_no. These two columns are created to combine any unit and street number that we already had, plus the ones we split afterwards   

To run this script, go into terminal and enter: `python 1-parse_csv.py merged.csv street_addr 1-parsed.csv`. If there is no module named postal, enter 'conda install postal' into the terminal

# combine_parsed_cols.py
This script's purpose is to merge columns together. As mentionned previously, some adresses were already split from data collection, so there are already some values in the columns street_no, street_name, etc. This script simply fills NAN values in these columns with values from LP2_street_no, LP_street_name, etc. 