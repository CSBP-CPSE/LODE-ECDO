"""
This scriptuses the validation version of the file, which still has the AGOL coordinates, to fill in missing CSDs
"""
import pandas as pd
import geopandas as gpd

df = pd.read_csv("../6-CSD_And_Clean/output/ODEFv2_ValidationFile_31-03-2021.csv", low_memory=False, dtype='str')

gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.X, df.Y))
gdf.crs="EPSG:4326"

#read in Statcan boundary file

CSD = gpd.read_file("/home/jovyan/data-vol-1/ODA/processing/3-Spatial_Group/CSD/lcsd000a16a_e.shp")
CSD=CSD[['CSDUID', 'CSDNAME','PRUID', 'geometry']]

#convert geometry of addresses to statcan geometry

gdf=gdf.to_crs(CSD.crs)


#perform spatial merge

gdf_csd=gpd.sjoin(gdf,CSD, op='within', how='left')

df=pd.DataFrame(gdf_csd)

df['CSDUID_left']=df['CSDUID_left'].fillna(df['CSDUID_right'])
df['CSDNAME_left']=df['CSDNAME_left'].fillna(df['CSDNAME_right'])

df=df.rename(columns={'CSDUID_left':'CSDUID', 'CSDNAME_left':'CSDNAME'})                  
df=df.drop(columns=['index_right','geometry'])
                  

df.to_csv('ODEF_Validation_ForDedupe.csv',index=False)
