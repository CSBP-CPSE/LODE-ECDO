# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:47:57 2020

@author: josep
"""

import pandas as pd

cihi1=pd.read_excel(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\Data sources\CIHI\CIHI-2020-03-30\CHRP Hospitals.xlsx")
cihi2=pd.read_excel(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\Data sources\CIHI\CIHI-2020-03-30\CHRP Hospitals v2.xlsx")
cihi2=cihi2[['SITE_NAME','POSTAL_CODE']]
CIHI=pd.merge(cihi1,cihi2,how='left',left_on='Postal_Code',right_on='POSTAL_CODE')



CIHI['FacilityName']=CIHI['SITE_NAME'].fillna(CIHI.HOSPITAL_NAME)


CIHI=CIHI[['HOSPITAL_NAME',
           'SITE_NAME',
           'FacilityName',
 'Address1',
 'Address2',
 'City',
 'Postal_Code',
 'Province',
 'Country',
 'AddressLine',
 'Municipality',
 'PostalCode',
 'Geocoding Score',
 'Longitude',
 'Latitude',
 'Residential',
 'CoordType',
 'AddrPointT']]
CIHI.to_csv('cihi_test.csv',index=False)