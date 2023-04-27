# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:25:11 2020

@author: josep
"""

import pandas as pd

#df=pd.read_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\CURRENT\healthfacilitiesproject-2020-04-05\workspace\04-dataset_ManualProcessing.csv",
 #              encoding='cp1252')
dataset_filename = r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\CURRENT\healthfacilitiesproject-2020-04-05\workspace\ODHF_Validation.xlsx"
df = pd.read_excel(dataset_filename)
#dupes=pd.read_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\CURRENT\healthfacilitiesproject-2020-04-05\workspace\dupes_naics.csv",
dupes=pd.read_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\CURRENT\healthfacilitiesproject-2020-04-05\workspace\hospital_match_indices.csv",encoding='cp1252')


#dupes=dupes.dropna(subset=['hospital_name','name_f'])

#make group ID
df['hosp_group']=0
g_id=1
IDS=list(df['index'])
for idx in df['index']:
    ivals=[]

    if df.loc[df['index']==idx,'hosp_group'].item()==0:
        g_id+=1
        ivals=[]
        temp=dupes.loc[(dupes['index']==idx)|(dupes['index_f']==idx)]

            
        if len(temp)==0:
            df.loc[df['index']==idx,'hosp_group']=g_id
        else: #get all index values that this index has been matched to
            for val in temp['index'].unique():
                ivals.append(val)
            for val in temp['index_f'].unique():
                ivals.append(val)
            ivals=list(set(ivals))
            print(ivals)
            #check if any of these values have already been assigned a group index
            g2=0
            for i in ivals:
                if i in IDS:
                    if df.loc[df['index']==i,'hosp_group'].item()!=0:
                        g2=df.loc[df['index']==i,'hosp_group'].item()
                        print(g2)

                        break
            if g2!=0:
                df.loc[df['index'].isin(ivals),'hosp_group']=g2
            else:
                df.loc[df['index'].isin(ivals),'hosp_group']=g_id
  #  else:
   #     for val in temp['index'].unique():
   #         ivals.append(val)
   #     for val in temp['index_f'].unique():
   #         ivals.append(val)
   #     ivals=list(set(ivals))
   #     df.loc[df['index'].isin(ivals),'hosp_group']=df.loc[df['index']==idx,'hosp_group'].item()

df.to_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\ODHF-snapshots\CURRENT\healthfacilitiesproject-2020-04-05\workspace/group_id_Hospitals.csv",index=False,encoding='cp1252')
            
        