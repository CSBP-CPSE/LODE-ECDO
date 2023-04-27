import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
import re
from datetime import datetime
from requests.auth import AuthBase


#%% Get and Scrape website

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url_start = 'https://www.easternhealth.ca/facilities/page/'


name = []
address = []
phone = []
city = []
postal_code = []
ftype = []

for i in range(1, 10):
    time.sleep(random.randint(1,4))
    page = requests.get(url_start+str(i)+'/', headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for names in soup.find_all('h2', {'class': 'geodir-entry-title'}):
        name.append(names.text)
    
    for boxes in soup.find_all('ul', {'class': 'geodir-category-list-view clearfix gridview_one geodir-listing-posts geodir-gridview gridview_one'}):
        for links in boxes.find_all('a'):
            time.sleep(3)
            # go through every link
            sec_page = requests.get(links['href'], headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
            sec_soup = BeautifulSoup(sec_page.content, 'html.parser')
            pretty2 = sec_soup.prettify()
            
            for sec_boxes in sec_soup.find_all('ul', {'class': 'contactdetailssidebar'}):
                address.append(sec_boxes.find('span', {'itemprop': 'streetAddress'}).text)
                city.append(sec_boxes.find('span', {'itemprop': 'addressLocality'}).text)
                
                if sec_boxes.find('span', {'itemprop': 'postalCode'}) is None:
                    postal_code.append(np.nan)
                else:
                    codes = sec_boxes.find('span', {'itemprop': 'postalCode'})
                    postal_code.append(codes.text)
                
                if sec_boxes.find('div', {'class': 'geodir_post_meta geodir-field-phone'}) is None:
                    phone.append(np.nan)
                else:
                    phones = sec_boxes.find('div', {'class': 'geodir_post_meta geodir-field-phone'})
                    phone.append(phones.find('a').text)
                    
                for ftypes in sec_boxes.find_all('div', {'class': 'geodir_post_meta geodir-field-post_category'}):
                    ftype.append(ftypes.find('a').text)
                    
                    
#%% Create DataFrame

columns = {'facility_name': name, 'street_addr': address, 'phone': phone, 'city': city, 'postal_code': postal_code, 'province': 'NL', 'facility_type': ftype}
df = pd.DataFrame(columns)

df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/NL_Eastern_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/NL_Eastern_health_facilities.csv', index=False)
​

                    