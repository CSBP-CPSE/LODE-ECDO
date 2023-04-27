#%% Import librairies

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
from requests.auth import AuthBase


#%% Get website

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url = 'https://yukon.ca/en/find-hospital-or-health-centre'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


#%% Scrape information

name = []
address = []
phone = []
fax = []

for facilities in soup.find_all("section", {"class": "block block-views clearfix"}):
    for links in facilities.find_all("a"):
        time.sleep(3)
        sec_page = requests.get('https://yukon.ca'+links['href'], headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
        sec_soup = BeautifulSoup(sec_page.content, 'html.parser')
        name.append(sec_soup.find("h1", {"class": "page-header"}).text)
        for address_boxes in sec_soup.find_all("div", {"class": "field field-name-field-places-address field-type-text field-label-above"}):
            address.append(address_boxes.find("div", {"class": "field-item even"}).text)
        for phone_boxes in sec_soup.find_all("div", {"class": "field field-name-field-places-telephone field-type-text field-label-above"}):
            phone.append(phone_boxes.find("div", {"class": "field-item even"}).text)
            
        if sec_soup.find("div", {"class": "field field-name-field-fax- field-type-text field-label-abovec"}) is None:
            fax.append(np.nan)
        else:
            fax_boxes = sec_soup.find("div", {"class": "field field-name-field-fax- field-type-text field-label-abovec"})
            fax.append(fax_boxes.find("div", {"class": "field-item even"}).text)


#%% Create DataFrame
            
columns = {'facility_name':name, 'street_addr':address, 'phone':phone, 'fax':fax}
df = pd.DataFrame(columns)
df['province'] = 'YT'

# categorize facilities based on name
hoskeywords = 'hospital'
ambkeywords = 'health centre'
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/YT_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/YT_health_facilities.csv', index=False)
                








