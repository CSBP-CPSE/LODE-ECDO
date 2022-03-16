# -*- coding: utf-8 -*-
"""
script to download data from esri rest end point
@author: kuchjos
"""

import requests
import json
import time



#Get total number of records
params1={'returnIDsOnly':'True',
         'where':'1=1',
         'f':'json'
        }
url="https://services.arcgis.com/mMUesHYPkXjaFGfS/ArcGIS/rest/services/Rural_Health_Care_Facilities_in_Manitoba/FeatureServer/0/query"
test=requests.get(url,
                    params=params1)

IDs=test.json()

IDs=IDs['objectIds']

"""
most APIs have a limit to number of entries you can query at once
so this loop makes requests in increments of 500 at a time
"""
chunk=500
start=0
N=len(IDs)
end=chunk
Addresses=[]
k=1
###
"""
this doesn't seem to work by passing lists:
should instead use queries based on object IDs, they seem to always be integers
something like, get list, sort list, check value of Nth, use that in query
"""
###

if N>end:
    ID_min=IDs[start]
    ID_max=IDs[end]
    stop=0
    while end<=N-1:
        print('working on chunk {} of {}'.format(k,int(N/chunk)))
        k+=1
        params2={'where':'objectId>={} and objectId<{}'.format(ID_min,ID_max+1),
                 'f':'geojson',
                 'outFields':'Community_Name,Facility_Name,Lat,Long,Emergency_Department_Availabili,Nearest_Alternate_Emergency_Dep,Acute_Care_Availability,Transitional_Care_Availability,Personal_Care_Home',
                 'returnGeometry':'True',
                 'GeometryType':'esriGeometryPoint'}
        #fix
        test2=requests.get(url,
                            params=params2)
        print(test2.status_code)
        adds=test2.json()
        #print(json.dumps(adds,indent=2))
        time.sleep(10)
        adds=test2.json()
        Addresses.append(adds)
        
        start=end
        end+=chunk
        if end>N-1:
            end=N-1
            stop+=1
        if stop>1:
            break
        ID_min=IDs[start]
        ID_max=IDs[end]
    
else:
    ID_min=IDs[start]
    ID_max=IDs[N-1]
    print('working on chunk {} of {}'.format(1,1))
        
    params2={'where':'objectId>={} and objectId<{}'.format(ID_min,ID_max+1),
             'f':'geojson',
                 'outFields':'Community_Name,Facility_Name,Lat,Long,Emergency_Department_Availabili,Nearest_Alternate_Emergency_Dep,Acute_Care_Availability,Transitional_Care_Availability,Personal_Care_Home',
                 'returnGeometry':'True',
                 'GeometryType':'esriGeometryPoint'}
        #fix
    test2=requests.get(url,
                            params=params2)
    print(test2.status_code)
    adds=test2.json()
        #print(json.dumps(adds,indent=2))
    adds=test2.json()
    Addresses.append(adds)
        
    

    #print(json.dumps(adds,indent=2))
#print(Addresses[0])

main_list=[]
for sublist in Addresses:
    for item in sublist:
        main_list.append(item)

with open('MB_RuralHealthCareFacilities.json','w') as f:
    json.dump(Addresses, f,indent=2)        