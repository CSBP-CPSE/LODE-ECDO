#%% Import librairies

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests.auth import AuthBase


#%% Get website

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url = 'https://www.ierha.ca/default.aspx?cid=6378&lang=1'
page = requests.get(url, headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
soup = BeautifulSoup(page.content, 'html.parser')
time.sleep(3)


#%% Scrape table

table = soup.findAll("table")[2]
df = pd.read_html(str(table))[0]


#%% Create DataFrame

df = df.dropna(how='all')
df = df.drop(columns=[3])
df = df.rename(columns={0:'city',1:'facility_name',2:'street_addr',4:'prephone'})

# extract phone numbers from information column and drop the now useless 'prephone' column
df['phone'] = df['prephone'].str.extract(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
df = df.drop(columns=['prephone'])
# clean the data in facility_name column
df['facility_name'] = df['facility_name'].str.strip('-')
df['facility_name'] = df['facility_name'].str.replace('\(Click for details\)', '', regex=True)
df['facility_name'] = df['facility_name'].str.replace('\(click for details\)', '', regex=True)
# there are two facilities that come up twice, here I am just moving the address from 
# one double to the other and dropping the first instances of each (check website to understand better)
df['street_addr'][37] = df['street_addr'][1]
df['street_addr'][38] = df['street_addr'][0]
df = df.drop(index=[0,1])
df['province'] = 'MB'

# categorize facilities based on name
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ambkeywords = 'centre|complex|campus|medical group|clinic|medicentres|community|health'
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/MB_Interlake_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/MB_Interlake_health_facilities.csv', index=False)

