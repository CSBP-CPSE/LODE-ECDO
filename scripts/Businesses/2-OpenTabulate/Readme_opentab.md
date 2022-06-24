# 2-OpenTabulate

## What is opentab? ##

Opentabulate is a script that is used to standardize column names across different datasets. Looking at all the datasets in /data/input, the same information in two datasets will have two different column names. Opentab is here to remedy this issue. 


## The variable map ##

The first step is creating a variable map (variablemap.csv). This is quite simple, the column headers in this file are the column names you want for a specific information, such as "facility_name" and "phone" (not all datasets need to contain this information). Each row in the variable map is a different dataset taken from /data/input/. So, for example, let's assume dataset_1 has a column header "HOSPITAL_NAME". In the variable map, in the row for that dataset, under the column "facility_name", we write "HOSPITAL_NAME". This will tell the program what information is what in each dataset (it can't guess for us... yet). By viewing the variable map, this explanation becomes clearer


## JSON Generator ##

Run `1-jsongenerator.ipynb` to create the JSONs necessary to run opentabulate

## Opentabulate ##

### 1. `data/input`
The files in `data/input` are a copy of all files from `1-PreProcessing/processed`

### 2. Configuration
The configuration file in this directory (`opentabulate.conf`) is just a copy of the one actually used by opentabulate. To run opentabulate, you will need to add or edit certain things to the configuration, but you must do this at the root of the system. To access the script at the root, go into the terminal and enter: 
`nano ~/.config/opentabulate.conf`
You can edit multiple things in opentab, but probably the most essential is the last section "labels". Here you can edit what column headers you want in the output, but it's very important that they must be the same as in the variable map. (You don't need to put all the labels that are in the variable map, but you cannot add any that are not in the variable map)
For more details on the different opentabulate settings as well as installation, visit: [https://opentabulate.readthedocs.io/en/latest/]

### 3. Running opentabulate
The variable map is done and the jsongenerator was run (with the JSON files are in /sources/), we are ready to run opentabulate. 
To get the output of only one dataset, enter in the terminal: `opentab sources/src-PE_Hospitals.json`
To get the output of all sources, enter in the terminal: `for file in sources/*; do opentab $file; done`

NOTE: For ODBiz, an alternative is to run the following commands in terminal:
```
$ cd /home/jovyan/ODBiz/2-OpenTabulate/sources
$ opentab *
```

### 4. The output
After running opentabulate, you will find the CSV files with the new column headers in /data/output

---

## `update_mapping_summary.py`
In order to ensure that columns get properly mapped by opentab, especially when dealing with a large number of datasets, the script `update_mapping_summary.py` will generate `mapping_summary.txt` and `unmapped_vars.csv`. `mapping_summary.txt` provides a summary of the column mappings that `variablemap.csv` will produce. It will also flag unmapped columns and unrecognized variables, which are variables present in variablemap, but not in the original dataset. `unmapped_vars.csv` displays unmapped columns in a slightly more readable format if opened in Excel.

## `add_filename.ipynb` ##
With the outputs, you can then run add_filename.ipynb to add a column with the name of the file this dataset comes from. This makes it easier to locate different facilities and where errors might come from later in the process.

NOTE: For ODBiz, `1-json_generator.ipynb` has been modified to tell opentab to perform what `add_filename.ipynb` does automatically.