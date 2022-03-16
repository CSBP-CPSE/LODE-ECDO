import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
import re
from datetime import datetime
from requests.auth import AuthBase


#%%

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url_start = 'https://wrha.mb.ca/locations-services/'
url_end = ['hospitals/', 'health-centres/', 'access-centres/', 'community-health-offices/']


name = []
info = []

for ends in url_end:
    time.sleep(3)
    page = requests.get(url_start+ends, headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for boxes1 in soup.find_all("div", {"class": "su-row"}):
        for names in boxes1.find_all(["strong", "b"]):
            name.append(names.text)
        for t1 in ["b", "strong"]:
            [s.extract() for s in boxes1(t1)]
        for infos in boxes1.find_all("p"):
            info.append(infos.text)
    for boxes2 in soup.find_all("div", {"class": "advgb-columns advgb-columns-row advgb-is-mobile advgb-columns-2 layout-12-12 mbl-layout-stacked vgutter-10"}):
        for names in boxes2.find_all(["strong", "b"]):
            name.append(names.text)
        for t2 in ["b", "strong"]:
            [s.extract() for s in boxes2(t2)]
        for infos in boxes2.find_all("p"):
            info.append(infos.text)

name.pop(18)


#%% Clean data

columns = {"facility_name": name, "info": info, "city": "Winnipeg", "province": "MB"}
df = pd.DataFrame(columns)
df['phone'] = df['info'].str.extract(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
df['website'] = df['info'].str.extract('site:(.*)')
df['info'] = df['info'].str.replace('\n', ' ')

df['street_addr'] = df['info'].str.extract('(.*)204')
df['street_addr'] = df['street_addr'].str.replace('Phone:', '')
df['street_addr'] = df['street_addr'].str.replace('Winnipeg', '')
df['street_addr'] = df['street_addr'].str.replace('Manitoba', '')
df['street_addr'] = df['street_addr'].str.replace('Churchill', '')
df['street_addr'] = df['street_addr'].str.replace('MB', '')

df = df.drop(columns=['info'])

# categorize facilities based on name
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ambkeywords = 'centre|complex|campus|health|ACCESS|WRHA|community|inkster|clinic'
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/MB_Winnipeg_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/MB_Winniped_health_facilities.csv', index=False)

