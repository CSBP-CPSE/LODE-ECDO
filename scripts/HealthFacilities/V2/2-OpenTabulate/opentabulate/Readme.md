This directory contains scripts to run opentabulate, which standardizes column headers between datasets. 

Open tabulate requires three components to run:
1. a configuration file: `opentabulate.conf`
2. CSV data file(s) to be mapped 
3. A json for each CSV to tell opentabulate how to map the column names from each dataset to a standardised set of column names.

Full docs for opentabulate are here: https://opentabulate.readthedocs.io/en/latest/

### Configuration

The configuration file in the reposity is just a copy of the one actually used by opentabulate. To run opentabulate, you will need to add/edit this configuration at the root of the system you are using. 

It could be found/edited here: `nano ~/.config/opentabulate.conf`

### Json file generation

The json files can be generated using the jsongenerator script. This script takes variablemap.csv as its input, which has been filled in manually to record the column names for each open data set.

The outputs of the generator script are json files stored in /sources.

The original json generator script is here: https://github.com/KHobbs3/infc-processing

### Running open tabulate

Follow installation and setup steps in the (docs)[https://opentabulate.readthedocs.io/en/latest/]

To run open tabulate
- Navigate to the 'opentabulate' directory
- Run for one file: `opentab sources/src-PE_Hospitals.json`
- Run for all files in /sources: `for file in sources/*; do opentab $file; done`

-Sam Lumley
Jan 2022

