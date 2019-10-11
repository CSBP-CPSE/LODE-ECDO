#preprocessing for Quebec
#read geojson, turn Point into long and lat, export csv
#remove commas from addresses
import geopandas as gpd
import pandas as pd

#read shapefile with geopandas into geodataframe
gdf=gpd.read_file('/home/csis/codes/OpenTabulate/Libraries/QC_Libraries.geoJSON')
gdf=pd.DataFrame(gdf)

def strip_point(x):
	t=x.strip('POINT (')
	t=t.rstrip(')')
	print(t)
	return t.split()

LONGS=[]
LATS=[]
for i in gdf.geometry:
	a=str(i)
	LONGS.append(strip_point(a)[0])
	LATS.append(strip_point(a)[1])
    
gdf["LONGITUDE"]=LONGS
gdf["LATITUDE"]=LATS    

gdf['Adresse']=gdf['Adresse'].str.replace(',','')

gdf.to_csv('/home/csis/codes/OpenTabulate/Libraries/QC_Libraries.csv')
