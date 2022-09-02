# 1-PreProcessing
The purpose of this step is to do some basic data cleaning, especially if certain datasets are especially troublesome for the rest of our pipeline to deal with.

## `preprocessing_main.ipynb`
Hitting "Run all" on this Jupyter notebook will run all the necessary scripts in the correct order. A lot of the documentation was already written in the file `preprocessing_main.ipynb`, so it will not be repeated here.

## `ODBizSources.csv`
The file `ODBizSources.csv` stores metadata about our source files, including links to the original sources. Our source files are stored in `/home/jovyan/ODBiz/1-PreProcessing/raw`.

---

## Dropped rows
The scripts below will drop entries if they meet certain conditions that we deem as being irrelevant given the scope of this project

### `process_vancouver.py`
The Vancouver dataset duplicates every approved business year after year. As a result, about 80% of it's entries are duplicates. So, this script detects all duplicate sets based on the following columns: `['BusinessName', 'Province', 'BusinessType', 'Unit', 'House', 'Street', 'City', 'Province', 'PostalCode', 'Country']`

The script keeps the most recent entry and removes all the other duplicates.

In addition, this script removes entries that do not have a valid Canadian province code (i.e., they reside in states/provinces outside of Canada)