#This pre-processes Gatineau libraries.
#The original source includes many public buildings, so we restrict to libraries

import pandas as pd


df=pd.read_csv('pl_of_int-qc-gatineau.csv')

df=df.loc[df["TYPE"]=="Incendie"]

    
def strip_point(x):
	t=x.strip('POINT (')
	t=t.rstrip(')')
	return t.split()

LONGS=[]
LATS=[]
for i in df.GEOM:
	a=str(i)
	if a !='nan':
    
		LONGS.append(strip_point(a)[0])
		LATS.append(strip_point(a)[1])
	else:
		LONGS.append('')
		LATS.append('')
df["LONGITUDE"]=LONGS
df["LATITUDE"]=LATS

f_out='/home/csis/codes/OpenTabulate/pddir/raw/QC_Gatineau_Fire.csv'
df.to_csv(f_out)
