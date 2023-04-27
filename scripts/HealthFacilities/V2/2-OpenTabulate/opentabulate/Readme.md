### What is opentab? ###

Opentabulate is a script that is used to standardize column names across different datasets. Looking at all the datasets in /data/input, the same information in two datasets will have two different column names. Opentab is here to remedy this issue. 


### The variable map ###

The first step is creating a variable map (variablemap.csv). This is quite simple, the column headers in this file are the column names you want for a specific information, such as "facility_name" and "phone" (not all datasets need to contain this information). Each row in the variable map is a different dataset taken from /data/input/. So, for example, let's assume dataset_1 has a column header "HOSPITAL_NAME". In the variable map, in the row for that dataset, under the column "facility_name", we write "HOSPITAL_NAME". This will tell the program what information is what in each dataset (it can't guess for us... yet). By viewing the variable map, this explanation becomes clearer


### The JSON generator ###

The JSON generator (jsongenerator.ipynb) uses the variable map to create JSON files for every dataset in that variable map. These JSON files can be be found in /sources/ but do not really provide any new information, they basically provide the information in the variable map in another format. More importantly however, the opentabulate script requires the JSON files to change the column headers.
To continue with running opentabulate, you must run the jsongenerator.ipynb to create all the JSON files.


### Opentabulate ###

1. Configuration
The configuration file in this directory (opentabulate.conf) is just a copy of the one actually used by opentabulate. To run opentabulate, you will need to add or edit certain things to the configuration, but you must do this at the root of the system. To access the script at the root, go into the terminal and enter: 
"nano ~/.config/opentabulate.conf"
You can edit multiple things in opentab, but probably the most essential is the last section "labels". Here you can edit what column headers you want in the output, but it's very important that they must be the same as in the variable map. (You don't need to put all the labels that are in the variable map, but you cannot add any that are not in the variable map)
For more details on the different opentabulate settings as well as installation, visit: [https://opentabulate.readthedocs.io/en/latest/]

2. Running opentabulate
The variable map is done and the jsongenerator was run (with the JSON files are in /sources/), we are ready to run opentabulate. 
To get the output of only one dataset, enter in the terminal: "opentab sources/src-PE_Hospitals.json"
To get the output of all sources, enter in the terminal: "for file in sources/*; do opentab $file; done"           $ 

3. The output
After running opentabulate, you will find the CSV files with the new column headers in /data/output


### add_filename.ipynb ###

With the outputs, you can then run add_filename.ipynb to add a column with the name of the file this dataset comes from. This makes it easier to locate different facilities and where errors might come from later in the process.