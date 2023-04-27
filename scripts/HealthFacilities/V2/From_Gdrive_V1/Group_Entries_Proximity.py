# -*- coding: utf-8 -*-
"""
This script reads in a file of objects with Latitude and Longitude columns,
and adds a column with a 'group number' to indicate objects within a given distance
of each other.

"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
from scipy.spatial import cKDTree  


df=pd.read_csv(r"F:\Accessibility\Libraries\Processing\Libraries_Process7.csv", encoding='cp1252')

#first we need to drop entries we couldn't geocode

def group_D(df_in,Distance):
    
    df=df_in.copy()
    #consider only entries with geocoordinates
    df=df.loc[~df.Latitude.isnull()]
    df['geometry']=df.apply(lambda z: Point(z.Longitude,z.Latitude),axis=1)
    df=gpd.GeoDataFrame(df)
    
    
    #assume lon/lats are standard wgs84
    df.crs={'init': 'epsg:4326'}
    
    
    #convert to statcan projection
    df=df.to_crs({'init': 'epsg:3347'})
    
    #find entries near each other for deduplication
    
    addr_arr = np.array(list(zip(df.geometry.x, df.geometry.y)) )
    
    
    tree=cKDTree(addr_arr)
    indices=tree.query_ball_tree(tree,r=Distance,p=2.)
    
    # group together libraries based on proximity
    i=0
    N=len(indices)
    group=[None]*N
    group_num=1
    for i in range(N):
        group_num+=1
        val=group_num
        L=indices[i]
        for k in L:
            if group[k]!=None:
                val=group[k]
                break
        for k in L:
            group[k]=val
        
    df['group']=group 
    df=pd.DataFrame(df)
    df=df.drop(columns=['geometry'])
    return df
