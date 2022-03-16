# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 07:39:08 2020

@author: josep
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

df=pd.read_excel(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\Scripts\ON_Validation.xlsx")

geometry = [Point(xy) for xy in zip(df.X, df.Y)]

gdf = gpd.GeoDataFrame(df, crs='epsg:4326', geometry=geometry)

df2=df[['UID','Latitude','Longitude']]

geometry = [Point(xy) for xy in zip(df2.Longitude, df2.Latitude)]

gdf2 = gpd.GeoDataFrame(df2, crs='epsg:4326', geometry=geometry)

gdf=gdf.to_crs('epsg:3347')
gdf2=gdf2.to_crs('epsg:3347')

temp=gdf.geometry.distance(gdf2.geometry)

gdf['Distance']=temp

DF=pd.DataFrame(gdf)

DF['ValidationPriority']=''

DF.loc[DF.Distance<20,'ValidationPriority']='Very Low'
DF.loc[(DF.Distance>20)&(DF.Distance<50),'ValidationPriority']='Low'
DF.loc[(DF.Distance>50)&(DF.Distance<100),'ValidationPriority']='High'
DF.loc[DF.Distance>100,'ValidationPriority']='Very High'


DF.to_csv('ON_Validation_Out.csv',index=False)
