#%% Import librairies

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from requests.auth import AuthBase


#%% Scrape website

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url_start = 'https://www.albertahealthservices.ca/findhealth/results.aspx?type=facility&id='
url_end = '&locationCity=Calgary&radius=all#contentStart'

name = []
address = []
phone = []

for i in range(1, 12):
    time.sleep(3)
    page = requests.get(url_start+str(i)+url_end, headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for names in soup.find_all("a", {"class": "gridTitle"}):
        name.append(names.text)
    for addresses in soup.find_all("p", {"class": "gridAddress"}):
        address.append(addresses.text)
    for phones in soup.find_all("p", {"class": "gridPhone"}):
        phone.append(phones.text)    


#%% Create DataFrame

columns = {'facility_name': name, 'street_addr': address, 'phone': phone, 'province': 'AB'}
df = pd.DataFrame(columns)

# categorize facilities based on name
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ambkeywords = 'centre|complex|campus|medical group|clinic|medicentres|community|health|nursing station|regional|'
ltckeywords = 'residence|residential|résidence|nursing|palliative|senior|special care|seinor|long term|hospice|C.H.S.L.D.|specialized care|long care|long-term|assisted|nursing|retirement|personal care|chronic|memorial home|wellness'
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'
df.loc[df['facility_type'].str.contains(ltckeywords, case=False, na=False), 'facility_type'] = 'Nursing and residential care facilities'

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/AB_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/AB_health_facilities.csv', index=False)
    