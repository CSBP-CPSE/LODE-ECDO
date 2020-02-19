# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 08:29:38 2020

@author: JosephKuchar

This script processes the address file from the Saskatoon open data portal
(http://opendata-saskatoon.cloudapp.net/DataBrowser/SaskatoonOpenDataCatalogueBeta/ParcelAddress#param=NOFILTER--DataView--Results)
it's a kml file with embedded html, so this parses different parts of the file
using either html or xml parsing
"""
import pandas as pd
from bs4 import BeautifulSoup as Soup

with open("Saskatoon/ParcelAddress.kml") as data:
    kml_soup = Soup(data, 'lxml-xml') # Parse as XML
NUMBER=[]
ADDRESS=[]
descriptions = kml_soup.find_all('description')[1:]
for description in descriptions:
    html_soup = Soup(description.text, 'lxml') # Parse as HTML
    
    num=html_soup.find("td",string='STREET_NUMBER').find_next("td").get_text()
    add=html_soup.find("td",string='ONLINE_ADDRESS').find_next("td").get_text()
    ADDRESS.append(add)
    NUMBER.append(num)


LON=[]
LAT=[]

points = kml_soup.find_all('coordinates')
for point in points:
    xy=point.get_text().split(',')
    
    LON.append(xy[0])
    LAT.append(xy[1])

STREET=ADDRESS.copy()

for i in range(len(STREET)):
    STREET[i]=STREET[i].strip(NUMBER[i]).strip()
    STREET[i]=STREET[i].rstrip(', Saskatoon, SK CA')

dict={'NUMBER':NUMBER, 'STREET':STREET,'ADDRESS':ADDRESS,'LON':LON,'LAT':LAT}

df=pd.DataFrame(dict)
df.to_csv('Saskatoon.csv',index=False)
