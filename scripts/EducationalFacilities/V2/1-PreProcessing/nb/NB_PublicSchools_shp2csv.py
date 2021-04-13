# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:27:58 2020

@author: Joseph Kuchar (joseph.kuchar@canada.ca)
"""

import pandas as pd
import geopandas as gpd

gdf=gpd.read_file(r"C:\Users\josep\Downloads\geonb_nbps-epnb_shp\geonb_nbps-epnb.shp")
gdf=gdf.to_crs("EPSG:4326")
gdf['latitude']=gdf.geometry.y
gdf['longitude']=gdf.geometry.x

df=pd.DataFrame(gdf)



df.to_csv('NB_PublicSchools_geonb.csv',index=False,encoding='cp1252')