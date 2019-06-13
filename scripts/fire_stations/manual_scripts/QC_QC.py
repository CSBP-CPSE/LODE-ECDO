#This pre-processes Quebec city libraries.
#The original source includes many public buildings, so we restrict to fire stations

import pandas as pd


df=pd.read_csv('pl_of_int-qc-quebec_city.csv')

df=df.loc[df["DESCRIPTION"]=="Casernes de pompiers"]

    
def strip_point(x):
	t=x.strip('POINT (')
	t=t.rstrip(')')
	return t.split()

LONGS=[]
LATS=[]
for i in df.GEOMETRIE:
	a=str(i)
	if a !='nan':
    
		LONGS.append(strip_point(a)[0])
		LATS.append(strip_point(a)[1])
	else:
		LONGS.append('')
		LATS.append('')
df["LONGITUDE"]=LONGS
df["LATITUDE"]=LATS

f_out='/home/csis/codes/OpenTabulate/pddir/raw/QC_QC_fire.csv'
df.to_csv(f_out)
