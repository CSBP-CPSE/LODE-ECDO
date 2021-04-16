# -*- coding: utf-8 -*-
"""
Facilities have already been geocoded with ESRI, but for locations missing addresses or otherwise not geocoded precisely,
we can try to supplement with OSM.
We are going to try to find everything with a Score less than 95 that also doesn't already have coordinates from the source.
In addition to a POI search, we also perform a search for just the city and province to make it easier to assign CSD
"""

#import requests
import json
import pandas as pd
import time

#import jellyfish


headers = {
    'User-Agent': 'Joseph Kuchar, Statistics Canada',
    'From': 'joseph.kuchar@canada.ca' 
    }
url='https://nominatim.openstreetmap.org/search?'

JSONS=[]
JSONS_CITIES=[]


df=pd.read_csv("ODEFv2_Geocoded_AGOL_29-03-2021.csv", low_memory=False,dtype="str")
"""
df['nom_request']=df['facility_name']+ ', '+ df['city']+', '+df.province+', '+'Canada'
df['nom_request_2']= df['city']+', '+df.province+', '+'Canada'
df['geo_source']=df.geo_source.fillna('')
    
reqs=list(df['nom_request'])
reqs2=list(df['nom_request_2'])

geo_source=list(df['geo_source'])

for i in range(len(reqs)):
    query=reqs[i]
    query2=reqs2[i]

    source=geo_source[i]
    
    if (source!=''):
        JSONS.append([])
        #JSONS_CITIES.append([])
    else:
        
        params={'q':query,
                'addressdetails':'1',
                'format':'json',
                'email':'joseph.kuchar@canada.ca'}
        time.sleep(6)
        coords=requests.get(url, 
                        params=params, headers=headers)
        resp=coords.json()
        if len(resp)>0:
            resp=resp[0]
        JSONS.append(resp)
        print(i)
        print(query)
        if resp!=[]:
            print(resp['display_name'])
            
        #repeat for just city and province
#        params={'q':query2,
#                'addressdetails':'1',
#                'format':'json',
#                'email':'joseph.kuchar@canada.ca'}
#        time.sleep(6)
#        coords=requests.get(url, 
#                        params=params,headers=headers)
#        resp=coords.json()
#        if len(resp)>0:
#            resp=resp[0]
#        JSONS_CITIES.append(resp)
#        print(i)
#        print(query2)
#        if resp!=[]:
#            print(resp['display_name'])
"""

#with open('Nominatim.json', 'w', encoding='utf-8') as f:
#    json.dump(JSONS, f, ensure_ascii=False, indent=4)
with open('Nominatim.json', 'r', encoding='utf-8') as f:
    JSONS=json.load(f)    
    

LATS=[]
LONS=[]
ADDR=[]
CITY=[]
PROV=[]
NAME=[]
TYPE=[]
COUNTRY=[]
POST=[]
CITY=[]
for element in JSONS:
    if element==[]:
        LATS.append('')
        LONS.append('')
        NAME.append('')
        ADDR.append('')
        PROV.append('')
        TYPE.append('')
        COUNTRY.append('')
        POST.append('')
        CITY.append('')
    else:
        if (element['address']['country_code']=='ca') and ('amenity' in element['address'].keys()):
            
                
            
            COUNTRY.append(element['address']['country_code'])
        
        
            LATS.append(element['lat'])
            LONS.append(element['lon'])
            ADDR.append(element['display_name'])
            if 'type' in element.keys():
                TYPE.append(element['type'])
            else:
                TYPE.append('')
        
            NAME.append(element['address']['amenity'])
        
            if 'state' in element.keys():
                PROV.append(element['address']['state'])
            else:
                PROV.append('')
            if 'postcode' in element['address']:
                POST.append(element['address']['postcode'])
            else:
                POST.append('')
            if 'city' in  element['address']:
                CITY.append(element['address']['city'])
            else:
                CITY.append('')
            
                
        else:
            LATS.append('')
            LONS.append('')
            NAME.append('')
            ADDR.append('')
            PROV.append('')
            TYPE.append('')
            COUNTRY.append('')
            CITY.append('')
            

            
df['osm_address']=ADDR
df['osm_name']=NAME
df['osm_lat']=LATS
df['osm_lon']=LONS
df['osm_prov']=PROV
df['osm_country']=COUNTRY
df['osm_type']=TYPE
df['osm_city']=CITY


df.to_csv("ODEFv2_Geocoded_AGOL_OSM_31-03-2021.csv", index=False)