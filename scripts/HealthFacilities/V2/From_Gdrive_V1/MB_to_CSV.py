# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:44:37 2020

@author: josep
"""
import pandas as pd
import json

LON=[]
LAT=[]
COMMUNITY=[]
FACILITY=[]
EMERGENCY=[]
ACUTE=[]
PERSONAL=[]
TRANSITIONAL=[]
with open(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\Scripts\MB_RuralHealthCareFacilities.json") as f:
        data=json.load(f)
        for D in data:
            for d in D['features']:
                LON.append(d['geometry']['coordinates'][0])
                LAT.append(d['geometry']['coordinates'][1])
                FACILITY.append(d['properties']['Facility_Name'])
                COMMUNITY.append(d['properties']['Community_Name'])
                EMERGENCY.append(d['properties']['Emergency_Department_Availabili'])
                ACUTE.append(d['properties']['Acute_Care_Availability'])
                TRANSITIONAL.append(d['properties']['Transitional_Care_Availability'])
                PERSONAL.append(d['properties']['Personal_Care_Home'])
                
                    
df=pd.DataFrame({'Name':FACILITY,'Community':COMMUNITY,'Emergency':EMERGENCY,
                 'Acute':ACUTE,'Transitional':TRANSITIONAL,'Personal':PERSONAL,
                 'Latitude':LAT,'Longitude':LON,'source':'Manitoba Rural Health Facilities'}, dtype='str')
    
df.to_csv('Manitoba_RuralHealthCareFacilities.csv',index=False,encoding='cp1252')