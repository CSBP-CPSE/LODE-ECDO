#This pre-processes Ontario libraries.
#The csv includes both street and mailing address,
#and in some instances the mailing address is just a box number (to go along with street address),
#and in other instances the mailing address is the full address and the street address is blank
#we'll just look for empty entries in street address, and copy over the corresponding
#mailing addresses.

import pandas as pd

df=pd.read_csv('/home/csis/codes/OpenTabulate/Libraries/ON_Libraries.csv',encoding='utf-8')


N=len(df["A1.9 Street Address"])
i=0
street=list(df["A1.9 Street Address"])
mail=list(df["A1.5 Mailing Address"])
while i<N:
    if pd.isnull(street[i])==True:
        street[i]=mail[i]
    i+=1
df["A1.9 Street Address"]=street
#print(street)
f_out='/home/csis/codes/OpenTabulate/pddir/raw/ON_Libraries.csv'
df.to_csv(f_out)
