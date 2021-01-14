# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 09:12:56 2021

@author: Joseph Kuchar (joseph.kuchar@canada.ca)

This just converts a geojson downloaded from the Vancouver open data portal to a shapefile,
as the openaddresses processing script struggled with the formatting of the geojson.
"""

import geopandas as gpd

gdf=gpd.read_file(r"C:\Users\josep\OneDrive\Work\ODA\pre-processing\vancouver-property-addresses.geojson")
gdf.to_file('vancouver-property-addresses.shp')

