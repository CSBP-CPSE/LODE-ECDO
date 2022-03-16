"""
This script reads in the sources CSV containing the list of open data portals 
Where a direct link to the data is available, it downloads the datasets 
into the raw directory

-Sam Lumley
Dec 2021

"""


import pandas as pd
import requests 

url = 'https://raw.githubusercontent.com/CSBP-CPSE/LODE-ECDO/odhfv2/sources/HealthFacilities/V2/ODHF_v2_Sources.csv'
df = pd.read_csv(url, index_col=0)

links = df['Direct link'].dropna()


# Loop through list and download csv files

for index, url in enumerate(links):
    req = requests.get(url)
    url_content = req.content
    
    filename = df['Filename'][index]
    
    csv_name = str(filename) + '.csv'
    csv_file = open(str(csv_name), 'wb')
    csv_file.write(url_content)
    csv_file.close()