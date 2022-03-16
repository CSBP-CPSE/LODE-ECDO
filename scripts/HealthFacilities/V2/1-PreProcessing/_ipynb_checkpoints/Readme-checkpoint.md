This directory contains scripts to download and tidy open data sources for health facilities. 

Download.py (and the .ipynb file) are used to download data from each of the open data sources as given in the ODHF source CSV, which is currently here: https://github.com/CSBP-CPSE/LODE-ECDO/tree/odhfv2/sources/HealthFacilities/V2

The downloaded data files are stored in /raw.

The processing.ipynb script processes the raw downloaded files for use with Open Tabulate into  /processed. The following steps are taken:
- Format latitude and longitude as separate columns
- Convert format to CSV 
- Encode CSV with utf-8
- Filter out data not related to health (eg police stations)

-Sam Lumley
Jan 2022

