# What is the goal of parsing in the project?
We have different formats for addresses. If you take a look at the `input/ODBiz_Merged.csv` file, you will notice that some addresses are all together under the full_address column, while some addresses are split into street_no, street_name, postal_code, etc. 

The objective is to split the addresses that are NOT split (which is the majority), and make individual columns for street number and name, unit number, city and postal code

## 0. parsing_main.ipynb
Hitting "Run all" on this Jupyter notebook will run all the necessary parsing scripts in the correct order as explained below

## 1. parse_csv.py
This python script's purpose is to separate the full addresses thanks to the pypostal library. New columns (LP_...) are created with the parsed addresses, WITHOUT including the addresses that were already split. The output of this file is parsed.csv. 

There exists an issue with the LP_street_no column: sometimes, full addresses will have unit number and street number separated with a dash (12-235, for example). The parsing code recognizes this as a full street number, instead of 2 different values, which is why we split these wherever necessary. This is why there are two additional columns in the parsed file: LP2_unit and LP2_street_no. These two columns are created to combine any unit and street number that we already had, plus the ones we split afterwards. Addionally, some entries have multiple values seperated with multiple dashes. We provide a spillover column for whenever this happens and it is later dealt with in `odbiz_custom_parse.py`.

To run this script, go into terminal and enter: `python parse_csv.py input/ODBiz_Merged.csv full_address output/parsed_biz.csv`. If there is no module named postal, enter `conda install postal` into the terminal

## 2. odbiz_custom_parse.py
In the `LP_street_no` column, some entries have multiple number and letter values that are seperated by multiple dashes (4-flr-777, for example). This script handles most of these odd cases.

There are also other various parsing errors that the first script produces for the odbiz dataset that this script attempts to fix as much as possible. Read `parsing_errors_documentation.md` for more details about the errors that were discovered in this step.

## 3. combine_parsed_cols.py
This script's purpose is to merge columns together. As mentionned previously, some adresses were already split from data collection, so there are already some values in the columns street_no, street_name, etc. This script simply fills NAN values in these columns with values from LP2_street_no, LP_street_name, etc. 

## Dropped rows
The scripts above will drop entries if they meet certain conditions that we deem as being irrelevant given the scope of this project:

### `parse_csv.py`
This script doesn't drop any rows.

### `odbiz_custom_parse.py`
If the column `full_address` was a full match with one of the following strings:
```
[
'-',                                  
'BUSINESS - OUT OF TOWN SQUAMISH',    
'BUSINESS - OUT OF TOWN',             
'NON-RESIDENT',                       
'BUSINESS-NON RESIDENT'     
]
```

then the entry was removed.

### `combine_parsed_cols.py`
This script doesn't drop any rows.





