
"""
For a beginner, this website was very fun to webscrape. The same information had 
consistent tags, and information was properly identified through classes. No manual 
data cleaning necessary at all. 
(This is all very sarcastic, enjoy reading through this)
"""

#%% Import librairies

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re 
from datetime import datetime
from requests.auth import AuthBase


#%% Get page
# the easy part

logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Mathieu Justino.\n'.format(datetime.now()))

url = 'https://northernhealthregion.com/our-locations/#1540668509106-d9d2c9b8-cb84'
page = requests.get(url, headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
soup = BeautifulSoup(page.content, 'html.parser')


#%% Scrape information

name = []
info = []

# the boxes that contained all the necessary information actually had a class
for boxes in soup.find_all("div", {"class": "wpb_text_column"}):
    time.sleep(3)
    
    """what we are doing here is removing all instances of these 2 tags. As will 
    become clear later, precise information such as phone numbers or addresses 
    have no classes within their tag so we must "cast a wide net" to capture 
    all the relevant information. These 2 tags contain nothing useful, but would 
    be caught in our "wide net" so we delete them now"""
    
    for t1 in ["h4", "li"]:
        [s.extract() for s in boxes(t1)]
        
    for headers in boxes.findAll("strong"):
        name.append(headers.text)
    # go through a few links that contain more facilities
    for links in boxes.find_all("a"):
        # the only links we want to open contain the word "details" in the text
        if "details" in links.text:
            sec_page = requests.get(links['href'], , headers={'user-agent': 'Statistics Canada Bot created by Mathieu Justino, from: mathieu.justino@statcan.gc.ca'})
            sec_soup = BeautifulSoup(sec_page.content, 'html.parser')
            # go through the boxes in the new pages
            for sec_boxes in sec_soup.findAll("div", {"class": "wpb_text_column"}):
                for sec_headers in sec_boxes.findAll("strong"):
                    name.append(sec_headers.text)
                # now that we gathered the names throught the "strong" tag, we will 
                # delete all instances of it and "a" tag because they don't contain any more useful info
                for t in ["strong", "a"]:
                    [s.extract() for s in sec_boxes(t)]
                # gather all the information for each facility (includes phone, fax, address)
                for sec_infos in sec_boxes.findAll("p"):
                    info.append(sec_infos.text)
    # now that we went through the external links, we can delete our two tags (as 
    # we did 5 lines above). We couldn;t do this before requesting the external links 
    # because these are contained in "a" tags
    for t2 in ["strong", "a"]:
        [s.extract() for s in boxes(t2)]
    for infos in boxes.findAll("p"):
        info.append(infos.text)


#%% Clean lists

# no matter how hard you try to filter tags, some websites will have the same for 
# different types of information. So, here we delete rows that are these strings or empty rows
while 'Click here for full details and contact information' in name: name.remove('Click here for full details and contact information') 
while '' in info: info.remove('') 
while 'Below is a list of health care service and facilities located in this community.' in info: info.remove('Below is a list of health care service and facilities located in this community.')
while '24 Long Term Care Beds' in info: info.remove('24 Long Term Care Beds')

# here, we remove these phrases that were included in some rows (but the row also 
# contains the name, so we do not delete the row)
name = [x.replace('(click here for Primary Care and Walk-In Clinic Hours)', '') for x in name]
name = [x.replace('(click here for Primary Care Clinic and Same Day Access Clinic Hours)', '') for x in name]  
name = [x.replace('(click here for Primary Care and Same Day Access Clinic Hours)', '') for x in name]
info = [x.replace('Thompson General Hospital – Lower Level', '') for x in info]
# strip whitespaces
info = [x.strip() for x in info]


#%% Split Information

phone = []
fax = []
address = []

"""
If you print(info), you will notice that the string comes with line breaks. 
This is useful here, for fax and phone we simply say, grab whatever comes after 
"Telephone:" or "Fax:". Two things to note: 
    1. Every row has a phone number, however they sometimes use "Telephone" or 
    "Phone" or "Tel". We make sure to identify all these possibilities. 
    2. Not every row has a fax, so we make sure to check if it does, and if it 
    does we insert NAN
"""
for strings in info:
    if 'hone' in strings:
        strip_phone = re.search('hone:(.*)', strings)
        phone.append(strip_phone.group(1))
    elif 'Tel' in strings:
        strip_phone = re.search('Tel:(.*)', strings)
        phone.append(strip_phone.group(1))
    
    if 'Fax:' in strings:
        strip_fax = re.search('Fax:(.*)', strings)
        fax.append(strip_fax.group(1))
    else:
        fax.append(np.nan)
    
    # here we remove the line breaks to then be able to grab the addresses, that 
    # ALWAYS come before the phone number. (we once again make sure to consider 
    # both ways they write identify the phone number)
    new_strings = strings.replace('\n', ' ')
    if 'Phone' in new_strings:
        strip_address = re.search('(.*)Phone', new_strings)
        address.append(strip_address.group(1))
    elif 'Tel' in new_strings:
        strip_address = re.search('(.*)Tel', new_strings)
        address.append(strip_address.group(1))



#%% Create DataFrame

columns = {'facility_name': name, 'street_addr': address, 'phone': phone, 'fax': fax, 'province': 'MB'}
df = pd.DataFrame(columns)

df['phone'] = df['phone'].str.strip()
df['fax'] = df['fax'].str.strip()
# extract phone numbers
df['phone'] = df['phone'].str.extract(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')

# categorize facilities based on name
hoskeywords = 'hospital|hôpital|hôpitaux|cancer'
ambkeywords = 'centre|complex|campus|medical group|clinic|medicentres|community|health|nursing station|regional'
ltckeywords = 'residence|residential|résidence|nursing|palliative|senior|special care|seinor|long term|hospice|C.H.S.L.D.|specialized care|long care|long-term|assisted|nursing|retirement|personal care|chronic|memorial home|wellness'
df.loc[df['facility_name'].str.contains(ambkeywords, case=False, na=False), 'facility_type'] = 'Ambulatory health care services'
df.loc[df['facility_name'].str.contains(hoskeywords, case=False, na=False), 'facility_type'] = 'Hospital'
df.loc[df['facility_type'].str.contains(ltckeywords, case=False, na=False), 'facility_type'] = 'Nursing and residential care facilities'


df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/output/MB_Northern_health_facilities.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/2-OpenTabulate/opentabulate/data/web_scraped/MB_Northern_health_facilities.csv', index=False)