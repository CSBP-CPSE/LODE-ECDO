# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 08:41:13 2020

@author: Joseph Kuchar
split address number ranges for Montreal address points,
downloaded from  , provided by Service Des Infrastructures Du Réseau
 Routier - Division de la géomatique of Montreal under a CC-BY 4.0 license
"""

import geopandas as gpd
import pandas as pd

#read in Montreal shape file

gdf=gpd.read_file(r"Montreal\adresse\ADRESSE.shp")
crs={'init': 'epsg:4326'}
gdf=gdf.to_crs(crs)
gdf['LON']=gdf.geometry.x
gdf['LAT']=gdf.geometry.y
df=pd.DataFrame(gdf)
df=df.drop(['geometry'], axis=1)

print(list(df))

NUM1=list(df['ADDR_DE'])
NUM2=list(df['ADDR_A'])
GEN=list(df["GENERIQUE"])
SPEC=list(df["SPECIFIQUE"])
LON=list(df['LON'])
LAT=list(df['LAT'])
            

N=len(df)
for i in range(N):
    num1=NUM1[i]
    num2=NUM2[i]
    while num2>num1:
        num1+=2
        
        NUM1.append(min(num2,num1))
        NUM2.append(num2)
        GEN.append(GEN[i])
        SPEC.append(SPEC[i])
        LON.append(LON[i])
        LAT.append(LAT[i])
        
        
dict={'NUMBER':NUM1,
      'NUMBER2':NUM2,
      'GENERIQUE':GEN,
      'SPECIFIQUE':SPEC,
      'LAT':LAT,
      'LON':LON}

DF=pd.DataFrame(dict)
DF['STREET']=DF['GENERIQUE']+' '+DF['SPECIFIQUE']
DF['STREET']=DF.STREET.str.strip(' ')
DF.to_csv('Montreal.csv',index=False)