"""This script just reads in the simple dupes and the annotated dupes file to determine which records need to be dropped from the dataset."""

import pandas as pd

df=pd.read_csv("../6-CSD_And_Clean/output/ODEFv2_31-03-2021.csv",low_memory=False,dtype=str, index_col='Index')

dupes1=pd.read_csv("output/simple_dupes.csv",low_memory=False, dtype=str)
dupes2=pd.read_csv("output/dupe_check_annotated_TRUE.csv",low_memory=False,dtype=str)

print(len(df))

print(len(dupes1))

df=df.drop(list(dupes1['idx']))

print(len(df))

#the second dupes file contains the one to keep, not drop, so we need to reverse it

to_drop=[]
ID1=list(dupes2['idx1'])
ID2=list(dupes2['idx2'])
KEEP=list(dupes2['idx_keep'])

for i in range(len(dupes2)):
    id1=ID1[i]
    id2=ID2[i]
    k=KEEP[i]
    
    if id1==k:
        to_drop.append(id2)
    elif id2==k:
        to_drop.append(id1)
    else:
        print('no match')
        
df=df.drop(to_drop)
print(len(dupes1)+len(dupes2))
print(len(df))

df.to_csv("output/ODEFv2_DupesDropped_07-04-2021.csv")