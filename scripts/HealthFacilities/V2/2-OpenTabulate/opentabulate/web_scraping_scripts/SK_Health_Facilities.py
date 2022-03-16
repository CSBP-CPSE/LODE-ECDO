#%% Import Librairies

import numpy as np
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

url = 'https://www.saskhealthauthority.ca/facilities-locations?search=&field_location%5Bdistance%5D%5Bfrom%5D=1000&field_location%5Bvalue%5D=&field_facility_type=All&field_service=All&field_locality=&sort_bef_combine=title_ASC&display=list&field_use_near_me=&search_location_geocode&sort_by=title&sort_order=ASC&page='


address = []
name = []
phone = []

# go through the 20 pages on the website
for i in range(0, 21):
    page = requests.get(url+str(i), headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
    soup = BeautifulSoup(page.content, 'html.parser')
    time.sleep(3)
    
    for boxes in soup.find_all("div", {"class": "l-nav-content__content-module"}):
        for addresses in boxes.find_all("p", {"class": "address"}):
            address.append(addresses.text)
        for name_boxes in boxes.find_all("div", {"class": "c-teaser__title"}):
            for names in name_boxes.find_all("span"):
                name.append(names.text)
        for phone_boxes in boxes.find_all("div", {"class": "c-teaser__desc"}):
            # we use if/else here because not every facility has a phone number, so we must insert a NAN in the list
            if phone_boxes.find("a") is None:
                phone.append(np.nan)
            else:
                phones = phone_boxes.find("a")
                phone.append(phones.text)
                
                
#%% Create DataFrame

columns = {'facility_name': name, 'street_addr': address, 'phone': phone}
df = pd.DataFrame(columns)
# strip the additional whitespaces (caused by /br lines in the HTML)
df['street_addr'] = df['street_addr'].str.strip()
df['street_addr'] = df['street_addr'].str.replace('\s+', ' ', regex=True)
df['province'] = 'SK'


# categorize facilities based on name
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ambkeywords = 'centre|complex|campus|medical group|clinic|medicentres|community|health|nursing station|regional|'
ltckeywords = 'residence|residential|résidence|nursing|palliative|senior|special care|seinor|long term|hospice|C.H.S.L.D.|specialized care|long care|long-term|assisted|nursing|retirement|personal care|chronic|memorial home|wellness|lodge|home|integrated care|LTC'
labkeywords = 'laboratory'
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_type'].str.contains(ltckeywords, case=False, na=False), 'facility_type'] = 'Nursing and residential care facilities'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'
df.loc[df['facility_type'].str.contains(labkeywords, case=False, na=False), 'facility_type'] = 'Laboratory'


df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/SK_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/SK_health_facilities.csv', index=False)








