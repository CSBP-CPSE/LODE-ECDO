#%% Import librairies

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from requests.auth import AuthBase


#%% Get website

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url = 'https://www.nshealth.ca/locations'
page = requests.get(url, headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
soup = BeautifulSoup(page.content, 'html.parser')


#%% Scrape information

# we append the information scraped into these lists to then create the dataframe
facility_name = []
street_addr = []
city = []
province = []
postal_code = []
info = []

for names in soup.findAll("h4", {"class": "location-profile__name"}):
    time.sleep(3)
    facility_name.append(names.text)
for addresses in soup.findAll("div", {"class": "thoroughfare"}):
    time.sleep(3)
    street_addr.append(addresses.text)
for cities in soup.findAll("span", {"class": "locality"}):
    time.sleep(3)
    city.append(cities.text)
for provinces in soup.findAll("span", {"class": "state"}):
    time.sleep(3)
    province.append(provinces.text)
for postals in soup.findAll("span", {"class": "postal-code"}):
    time.sleep(3)
    postal_code.append(postals.text)
for infos in soup.findAll("div", {"class": "location-profile__description-telephone"}):
    time.sleep(3)
    info.append(infos.text)


#%% Create DataFrame

columns = {'facility_name':facility_name, 'street_addr':street_addr, 'postal_code':postal_code, 'city':city, 'province':province, 'info':info}
df = pd.DataFrame(columns)

# extract phone numbers from info column and drop info column
df['phone'] = df['info'].str.extract(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
df = df.drop(columns=['info'])

# categorize facilities based on name
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ambkeywords = 'centre|complex|campus|medical group|clinic|medicentres|community|health|blood| '
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/NS_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/NS_health_facilities.csv', index=False)