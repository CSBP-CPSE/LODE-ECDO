# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 08:41:13 2020
@author: Joseph Kuchar
split address number ranges for Montreal address points,
downloaded from  https://donnees.montreal.ca/ville-de-montreal/adresses-ponctuelles,
provided by Service Des Infrastructures Du Réseau
 Routier - Division de la géomatique of Montreal under a CC-BY 4.0 license
"""

import geopandas as gpd
import pandas as pd

#read in Montreal shape file

gdf=gpd.read_file(r"adresses.json", low_memory=False)
crs='epsg:4326'
gdf=gdf.to_crs(crs)
gdf['LON']=gdf.geometry.x
gdf['LAT']=gdf.geometry.y
df=pd.DataFrame(gdf)
df=df.drop(['geometry'], axis=1)
df['ORIENTATIO']=df['ORIENTATIO'].str.replace('X','')

print(list(df))

NUM1=list(df['ADDR_DE'])
NUM2=list(df['ADDR_A'])
GEN=list(df["GENERIQUE"])
SPEC=list(df["SPECIFIQUE"])
LON=list(df['LON'])
LAT=list(df['LAT'])
DIR=list(df['ORIENTATIO'])
LIEN=list(df['LIEN'])

            

N=len(df)
for i in range(N):
    num1=NUM1[i]
    num2=NUM2[i]
    
    #a couple of entries have numbers with 1/2 in them
    
    if '1/2' in num2:

        
        NUM1.append(str(num1)+' 1/2')
        NUM2.append(num2)
        GEN.append(GEN[i])
        SPEC.append(SPEC[i])
        LON.append(LON[i])
        LAT.append(LAT[i])
        DIR.append(DIR[i])
        LIEN.append(LIEN[i])
    else:
        num1=int(num1)
        num2=int(num2)
        while num2>num1:
            num1+=2

            NUM1.append(min(num2,num1))
            NUM2.append(num2)
            GEN.append(GEN[i])
            SPEC.append(SPEC[i])
            LON.append(LON[i])
            LAT.append(LAT[i])
            DIR.append(DIR[i])
            LIEN.append(LIEN[i])

dict={'NUMBER':NUM1,
      'NUMBER2':NUM2,
      'GENERIQUE':GEN,
      'SPECIFIQUE':SPEC,
      'LIEN': LIEN,
      'ORIENTATION': DIR,
      'LAT':LAT,
      'LON':LON}

DF=pd.DataFrame(dict)
                     
DF=DF.sort_values(by=['SPECIFIQUE','NUMBER'],ascending=True)
                                    
DF.to_csv('Montreal_16-04-2021.csv',index=False)