#%% Import librairies

import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
import re
from datetime import datetime
from requests.auth import AuthBase


#%% Get website and Scrape information

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url = 'https://wrha.mb.ca/long-term-care/pchs-in-winnipeg/'
page = requests.get(url, headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
soup = BeautifulSoup(page.content, 'html.parser')

name = []
info = []

box = soup.find("section", {"class": "entry-content"})
for links in box.find_all("a"):
    time.sleep(3)
    # go through every link
    sec_page = requests.get(links['href'], headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
    sec_soup = BeautifulSoup(sec_page.content, 'html.parser')
    
    name.append(sec_soup.find("h1").text)
    
    for infos in sec_soup.find_all("section", {"class": "entry-content"}):
        info.append(infos.find("p").text)
        

#%% Clean data

phone = []
fax = []
address = []
website = []

# the "info" list contains many different pieces of information, here we split all these up
for strings in info:
    
    strip_phone = re.search('Tel:(.*)', strings)
    phone.append(strip_phone.group(1))
    
    if 'Fax:' in strings:
        strip_fax = re.search('Fax:(.*)', strings)
        fax.append(strip_fax.group(1))
    elif 'fax:' in strings:
        strip_fax = re.search('fax:(.*)', strings)
        fax.append(strip_fax.group(1))
        
    website.append(strings.splitlines()[-1])
        
    new_strings = strings.replace('\n', ' ')
    
    strip_address = re.search('(.*)Tel', new_strings)
    address.append(strip_address.group(1))


#%% Create DataFrame 

columns = {'facility_name': name, 'street_addr': address, 'phone': phone, 'fax': fax, 'website': website, 'city': 'Winnipeg', 'province': 'MB', 'facility_type': 'long-term care'}
df = pd.DataFrame(columns)

# final cleaning of columns
df['fax'] = df['fax'].str.strip()
df.loc[df['fax'].str.contains('.ca'), 'fax'] = ''

df.loc[df['website'].str.contains('ax:'), 'website'] = ''
df.loc[df['phone'].str.contains('ax:'), 'phone'] = ''
df['street_addr'] = df['street_addr'].str.replace('Winnipeg', '')
df['street_addr'] = df['street_addr'].str.replace(' MB', '')

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/MB_Winnipeg_long_term_care.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/MB_Winniped_long_term_care.csv', index=False)

















