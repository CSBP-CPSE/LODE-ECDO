"""
Address - Building Linkage Version 2 - SCIEU

General approach: 
    This is a simpler version of the address/building link. The idea is to consider buildings, 
    DB-by-DB, and find nearest neighbour pairs only within DBs. then for each nearest neighbour,
    check to see if it's contained (distance 0) or not
Last edited by joseph, Aug. 26 2019
"""
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from scipy.spatial import cKDTree  

prov='BC'

print('Reading in building polygons...')

polys=gpd.read_file(r'building.shp') #provincial file of building footprints with DBUID assigned

polys=polys.loc[polys.Shape_Area.astype(float)>50]

#polys=polys[['geometry','Build_ID','DBUID']]
#polys=polys.rename(columns={'DBUID':'DBUID_bld'})
print('read in address file...')

adds=pd.read_csv('',encoding='cp1252', low_memory=False) # address point file with DBUID column
adds['geometry']=adds.apply(lambda z: Point(z.LON,z.LAT),axis=1)
adds=adds.dropna(subset=['DBUID'])
adds=gpd.GeoDataFrame(adds)
adds.crs={'init': 'epsg:4326'}
#change to statcan projection
adds=adds.to_crs(polys.crs)
#adds=adds.rename(columns={'DBUID':'DBUID_add'})
adds.DBUID=adds.DBUID.astype(str).str.rstrip('.0')


## Step 1: get list of DBUIDS that have both addresses and buildings

DBS=list(set(polys.DBUID.unique()) & set(adds.DBUID.unique()))
print(len(DBS),len(polys.DBUID.unique()),len(adds.DBUID.unique()))


## Step 2: Nearest Neighbors
N=len(DBS)
print('computing nearest neighbours...')
DFS=[]
count=1
for DB in DBS:
    print('DB ', count, 'of ', N)
    count+=1
    temp_adds=adds.loc[adds.DBUID==DB]
    temp_polys=polys.loc[polys.DBUID==DB]
    poly_arr = np.array(list(zip(temp_polys.centroid.x, temp_polys.centroid.y)) )
    addr_arr = np.array(list(zip(temp_adds.geometry.x, temp_adds.geometry.y)) )
    
    P_tree=cKDTree(poly_arr)
    A_tree=cKDTree(addr_arr)
    Distances1,indices1=P_tree.query(addr_arr)
    Distances2,indices2=A_tree.query(poly_arr)



    ## Step 2b: For the NNs, determine the actual distance from polygon to point (not centroid to point)
    build_id=[]
    area=[]
    Distances=[]
    #temp['Distances']=Distances
    
    for i in range(len(indices1)):
        index=indices1[i]
        
        #compute real distance
        #first check if address contained in polygon
        if temp_polys.geometry.iloc[index].contains(temp_adds.geometry.iloc[i]):
            d=0
        else:
            d=temp_polys.geometry.iloc[index].distance(temp_adds.geometry.iloc[i])
        Distances.append(d)
        build_id.append(temp_polys.Build_ID.iloc[index])
        area.append(temp_polys.Shape_Area.iloc[index])
        
    
    temp_df=temp_adds.copy()
    temp_df['Build_ID']=build_id
    temp_df['Area']=area
    temp_df['Distance']=Distances
    
    #DFS.append(temp_df)
    
    
    #We should also find nearest addresses to polygons.
    
    
    
    build_id=[]
    lons,lats,nums,streets,units,cities,dbuids,hashes=[],[],[],[],[],[],[],[]
    Distances=[]
    areas=[]
    CSDnames=[]
    CSDUIDs=[]
    
    #temp['Distances']=Distances
    for i in range(len(indices2)):
        index=indices2[i]
        lons.append(temp_adds.LON.iloc[index])
        lats.append(temp_adds.LAT.iloc[index])
        nums.append(temp_adds.NUMBER.iloc[index])
        streets.append(temp_adds.STREET.iloc[index])
        units.append(temp_adds.UNIT.iloc[index])
        cities.append(temp_adds.CITY.iloc[index])
        dbuids.append(temp_adds.DBUID.iloc[index])
        hashes.append(temp_adds.HASH.iloc[index])
        CSDnames.append(temp_adds.CSDNAME.iloc[index])
        CSDUIDs.append(temp_adds.CSDUID.iloc[index])

        areas.append(temp_polys.Shape_Area.iloc[i])
    
        #compute real distance
        if temp_adds.geometry.iloc[index].within(temp_polys.geometry.iloc[i]):
            d=0
        else:
            d=temp_adds.geometry.iloc[index].distance(temp_polys.geometry.iloc[i])
        #        print(d)
        Distances.append(d)
          
        build_id.append(temp_polys.Build_ID.iloc[i])
            
    temp2=pd.DataFrame({'LON':lons,'LAT':lats,'NUMBER':nums,'STREET':streets,'UNIT':units,'CITY':cities,
                        'Build_ID':build_id,'Distance':Distances,'DBUID':dbuids,'HASH':hashes, 'Area':areas,
                        'CSDUID':CSDUIDs,'CSDNAME':CSDnames})

    temp_df=temp_df.append(temp2, sort=True)
    temp_df=temp_df.drop_duplicates(subset=['Build_ID','HASH'])
    DFS.append(temp_df)


final=pd.concat(DFS, sort=True)
final=final.drop(columns=['DISTRICT','geometry'])
final=final[['DBUID','Build_ID','Distance','NUMBER','STREET','UNIT','CITY','CSDUID','CSDNAME','LON','LAT','Area','HASH']]
final.to_csv('Output/'+prov+'_merged_bothways.csv',index=False,encoding='cp1252')


"""
print('generating basic statistics')
final=final.loc[final.Distance<threshhold]
num_adds=len(adds)
num_bld=len(polys)
adds_with_bld=final.addr_uid.nunique()
blds_with_add=final.Build_ID.nunique()
address_with_multiple_blds = final.groupby(['addr_uid']).size().reset_index(name='count')
address_with_multiple_blds=len(address_with_multiple_blds.loc[address_with_multiple_blds['count']>1])
blds_with_multiple_address =final.groupby(['Build_ID']).size().reset_index(name='count')
blds_with_multiple_address=len(blds_with_multiple_address.loc[blds_with_multiple_address['count']>1])
with open('basicstats_bothways.txt','a') as file:
    file.write("{},{},{},{},{},{},{},{}\n".format(prov,num_bld,num_adds,adds_with_bld,blds_with_add,adds_inside_blds,blds_with_multiple_address,address_with_multiple_blds))
"""
