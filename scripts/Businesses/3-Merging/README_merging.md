# 3-Merging
The purpose of this step is to combine all our datasets, which are currently spread throughout multiple csvs, into one csv. Some more cleaning is also performed at this step since it's a lot easier to clean our entire dataset than it is to clean several csvs individually first and then merge them together

# merging_main.ipynb
Hitting "Run all" on this Jupyter notebook will run all the necessary scripts in the correct order as explained below

## `MergingBiz.py`
This script reads in, then merges all the output data from the 2-OpenTabulate/Output folder except for specified excluded files. It cleans and standardizes some columns and performs basic deduplication.

## `RemoveInvalidCoordinates.py`
Sets invalid coordinates to blank values to indicate that an entry needs to be geocoded.

## `FilterNoAddrInfo`
Removes entries with insufficient address info for geocoding

## `fix_NAICS_codes`
Cleans up the primary NAICS code column

---

## Dropped rows
The scripts below will drop entries if they meet certain conditions that we deem as being irrelevant given the scope of this project

### `MergingBiz.py`
This script performs basic deduplication. If a set of rows have exact matches with ALL of the following columns, then only one row is kept in the set, the script tries to keep the most recent row:
- 'business_name',
- 'licence_number',
- 'business_id_no',
- 'primary_NAICS',
- 'full_address',
- 'full_address_2',
- 'province',
- 'business_sector',
- 'licence_type'

### `RemoveInvalidCoordinates.py`
This script doesn't drop any rows, it simply flags rows that have invalid coordinates by setting their coordinate values as blank.

### `FilterNoAddrInfo`
This script checks the following columns:
- 'full_address',
- 'full_address_2',
- 'mailing_address',
- 'unit',
- 'street_no',
- 'street_name',
- 'street_direction',
- 'street_type',
- 'city',
- 'postal_code'

If ALL of the above columns are blank/NA, then the row is removed. 

### `fix_NAICS_codes`
This script doesn't drop any rows.

