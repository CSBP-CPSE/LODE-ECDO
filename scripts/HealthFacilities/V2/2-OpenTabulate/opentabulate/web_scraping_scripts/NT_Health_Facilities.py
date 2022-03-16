#%% Import librairies

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime
from requests.auth import AuthBase


#%% Request website

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url = 'https://www.hss.gov.nt.ca/en/hospitals-and-health-centres'
page = requests.get(url, headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
soup = BeautifulSoup(page.content, 'html.parser')


#%% Scrape information

name = []
info = []

for box in soup.find_all("div", {"class": "field-item even"}):
    time.sleep(3)
    for names in box.find_all(["h2", "h3"]):
        name.append(names.text)
    for infos in box.find_all("p"):
        info.append(infos.text)
        

#%% Split information
# the scraped list "info" contains address, fax and phone number. Here I split and compile the information in 3 lists

phone = []
fax = []
address = []

# the list's first 2 elements are irrelevant so I delete them
del info[0:2]

for strings in info:
    strip_phone = re.search('Phone:(.*)Fax', strings)
    phone.append(strip_phone.group(1))
    strip_fax = re.search('Fax:(.*)Address', strings)
    fax.append(strip_fax.group(1))
    strip_address = re.search('Address:(.*)', strings)
    address.append(strip_address.group(1))

# the list "name" contains duplicates, which I remove here (not exactly duplicates, but it's important to remove some to keep the lists the same length)
indexes = [0, 1, 12, 16, 20, 37]
for index in sorted(indexes, reverse=True):
    del name[index]
    

#%% Create DataFrame
    
columns = {'facility_name': name, 'street_addr': address, 'phone': phone, 'fax': fax}
df = pd.DataFrame(columns)
df['province'] = 'NT'

# categorize facilities based on name
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ambkeywords = ''
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'

df['street_addr'] = df['street_addr'].str.replace('General Delivery', '', regex=True)

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/NT_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/NT_health_facilities.csv', index=False)