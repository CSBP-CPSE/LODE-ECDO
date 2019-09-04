import geopandas as gpd
from geopandas.tools import sjoin
from shapely import wkt
import pandas as pd


pr='61' #province id
#read shapefile with geopandas into geodataframe - ODB
print('reading in ODB...')
odb=gpd.read_file('odb_northwestterritories.shp')

#read geojson from microsoft
print('reading in Bing Buildings...')
ms=gpd.read_file('Buildings/Microsoft/NorthwestTerritories.geojson')
#convert ms data to statcan projection
print('change projection...')
crs={'init':'epsg:3347'}
ms=ms.to_crs(crs)

#the ms data has no features besides geometry
#so workflow should be
#1. Find intersection with ODB and remove those buildings
#2. Read in csd geometry file to assign CSDs
#3. Calculate centroids, areas, perimeters
#4. Assign provider (Microsoft or Bing Maps)
#5. Merge

#1. Find intersection 
print('finding intersections...')
intersections=sjoin(ms,odb,how='inner',op='intersects')['geometry']

#merge and drop duplicates
#this isn't an ideal approach - normal pandas merge/dedupe doesn't work with geodataframes
#instead, add all polygons to dataframe, keep unique ones, then make new geodataframe

intersections=pd.DataFrame(intersections).astype(str)
ms=pd.DataFrame(ms).astype(str)

merged=pd.concat([intersections,ms]).drop_duplicates(subset='geometry',keep=False)
merged=gpd.GeoDataFrame(merged, crs=odb.crs)
merged['geometry']=merged['geometry'].apply(wkt.loads) #wkt converts string "POLYGON (...)" to polygon type

#2. Read in CSD file

print('reading in statcan geometries...')
csd=gpd.read_file('/home/csis/codes/StatCanBounds/lcsd000b16a_e.shp')
#restrict to prov/territory under consideration
csd=csd.loc[csd['PRUID']==pr]
#drop unnecessary columns
csd=csd[['CSDUID','CSDNAME','geometry']]

#spatial joins on polygons is memory intensive - instead, compute centroids and place them into csds
merged['centroid']=merged.centroid
#make copy of polygon column to not accidentally overwrite when we change geometry
merged['polys']=merged.geometry
merged=merged.set_geometry('centroid')

print('performing join on CSDs...')

#join polygon centroids to csds
centroids_csds=sjoin(merged,csd,how='left',op='within')

#3-4. Determine fill in Longitude, latitude, area, length, and provider columns
centroids_csds['Longitude']=centroids_csds.centroid.x
centroids_csds['Latitude']=centroids_csds.centroid.y
centroids_csds.set_geometry('polys')

centroids_csds=centroids_csds[['geometry', 'CSDUID', 'CSDNAME', 'Longitude', 'Latitude']]
#somehow, it has lost its geometry here and become a normal dataframe
centroids_csds=gpd.GeoDataFrame(centroids_csds, crs=odb.crs)
centroids_csds.set_geometry=centroids_csds['geometry']

centroids_csds['Shape_Area']=centroids_csds.geometry.area
centroids_csds['Shape_Leng']=centroids_csds.geometry.length
centroids_csds['Data_prov']='Microsoft'

#5. concatenate data files
centroids_csds=pd.DataFrame(centroids_csds).astype(str)
odb=pd.DataFrame(odb).astype(str)
merged_final=pd.concat([odb,centroids_csds], sort=False)
merged_final=gpd.GeoDataFrame(merged_final,crs=crs)
merged_final['geometry']=merged_final['geometry'].apply(wkt.loads)
N=len(merged_final.geometry)
merged_final['Build_ID']=range(1,N+1)
#merged_final['Shape_Len']=pd.to_numeric(merged_final['Shape_Len'])

print('outputting file')
merged_final.to_file('MERGED_NWT.shp',driver='ESRI Shapefile')

