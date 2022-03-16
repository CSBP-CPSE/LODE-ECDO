"""
the odef.geocoded.agol file is what was received from SGC after they geocoded it. It was also deduplicated by DIID
"""
import pandas as pd
import geopandas as gpd

df=pd.read_csv("ODHFv2_Geocoded_OSM_15-02-2022.csv", low_memory=False, dtype='str')


gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
gdf.crs="EPSG:4326"

#read in Statcan boundary file

CSD = gpd.read_file("../6-AssignCSDs/CSD_shapefile/lcsd000a16a_e.shx")
CSD=CSD[['CSDUID', 'CSDNAME','PRUID', 'geometry']]
#convert geometry of addresses to statcan geometry


gdf=gdf.to_crs(CSD.crs)


#perform spatial merge

gdf_csd=gpd.sjoin(gdf,CSD, predicate='within', how='left')

df=pd.DataFrame(gdf_csd)
df.to_csv('assigned_CSDs.csv', index=False)
df.to_csv('/home/jovyan/data-vol-1/ODHF/LODE-ECDO/scripts/HealthFacilities/V2/7-Deduplication/inputs/assigned_CSDs.csv', index=False)

'''
#merge parsed columns with other columns

df['postal_code'] = df['postal_code'].fillna(df['LP_PostCode'].str.upper())
df['city'] = df['city'].fillna(df['LP_City'].str.capitalize())
df['unit'] = df["LP_Unit"].str.capitalize()

#Fill nulls in facility type with authority type to collapse to single column

#df['facility_type'] = df['facility_type'].fillna(df['authority_type'])


df=df.drop(columns=['index_right','geometry','nom_request','nom_request_2','osm_prov',
                   'LP_City','LP_PostCode','LP_Province','LP_Unit','temp'])

df.to_csv("output/ODEFv2_ValidationFile_31-03-2021.csv",index=False, encoding="utf-8")

df = df.drop(columns=[ 'Score','Addr_type','X','Y',
                'osm_address',	'osm_lat',	'osm_lon',	'osm_name',	'osm_country',	'osm_type',
                 'keep', 'fuzzy_score', 'idx_basic', 'telephone','grade_range','grade_type', 'street_addr', 'authority_type'])
#final renaming of columns

column_map={"facility_name": "Facility_Name",
           "idx": "Index",
           "source_id": "Source_ID",
           "facility_type": "Facility_Type",
            'authority_name': "Authority_Name",
            'address_str': "Full_Addr",
            'city': "City", 
            'province': "Prov_Terr", 
            'postal_code': "Postal_Code", 
            'provider': "Provider", 
            'latitude': "Latitude", 
            'longitude': "Longitude", 
            'geo_source': "Geo_Source", 
            'street_no': "Street_No", 
            'street_name': "Street_Name", 
            'ISCED4+': "ISCED4Plus",
            'unit': "Unit"}


df=df.rename(columns=column_map)

"""Finally, this is where some hard-coded cleaning takes place to fix issues identified during validation"""
"""First, LLoyminster (on border of AB and SK) has records in AB but with Province saying SK"""

df.loc[(df.Provider=='Province of Saskatchewan') & (df['PRUID']=='48'), 'Prov_Terr'] = 'AB'


"""At least one record was mis-geocoded, if others are identified they can be added to the list"""

indices=['9b5765dc757079c8a5de']

df.loc[df['Index'].isin(indices),'Latitude']=''
df.loc[df['Index'].isin(indices),'Longitude']=''
df.loc[df['Index'].isin(indices),'Geo_Source']=''
df.loc[df['Index'].isin(indices),'CSDUID']=''
df.loc[df['Index'].isin(indices),'CSDNAME']=''
df.loc[df['Index'].isin(indices),'PRUID']=''


#########################################################

#fill in blanks in PRuid

df['PRUID2'] = ''
pr_dict={'NL': '10',
        'PE': '11',
        'NS': '12',
        'NB': '13',
        'QC': '24',
        'ON': '35',
        'MB': '46',
        'SK': '47',
        'AB': '48',
        'BC': '59',
        'YT': '60',
        'NT': '61',
        'NU': '62'
        }
for k in pr_dict.keys():
    df.loc[df.Prov_Terr==k,'PRUID2']=pr_dict[k]
    
df['PRUID']=df['PRUID'].fillna(df['PRUID2'])




df=df[['Index', 'Source_ID', 'Facility_Name', 'Facility_Type', 'Authority_Name', 'ISCED010', 'ISCED020', 'ISCED1', 'ISCED2', 'ISCED3', 'ISCED4Plus', 'Full_Addr', 'Unit','Street_No','Street_Name', 'City', 'Prov_Terr', 'Postal_Code', 'Provider', 'Latitude', 'Longitude', 'Geo_Source', 'CSDUID', 'CSDNAME', 'PRUID']]




df.to_csv('output/ODEFv2_31-03-2021.csv', index=False)
'''