#pre-processing for Longueuil library data
#read shapefile, output csv
#limit ourselves to hospitals
#Also turn 'POINT' Geometry into lat and lon

import geopandas as gpd
import pandas as pd

#read shapefile with geopandas into geodataframe
sc1=gpd.read_file('/home/csis/codes/OpenTabulate/Libraries/Bibliotheque.shp')

sc1=pd.DataFrame(sc1)

print(list(sc1))


def strip_point(x):

	x=str(x)    
	t=x.strip('POINT (')
	t=t.rstrip(')')
	print(t)
	return t.split()

LONGS=[]
LATS=[]
for i in sc1.geometry:
	LONGS.append(strip_point(i)[0])
	LATS.append(strip_point(i)[1])

sc1["LONGITUDE"]=LONGS
sc1["LATITUDE"]=LATS

print(sc1)
sc1.to_csv('/home/csis/codes/OpenTabulate/Libraries/QC_Longueuil.csv')
