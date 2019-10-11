#This pre-processes Quebec city libraries.
#The original source includes many public buildings, so we restrict to libraries

import pandas as pd


df=pd.read_csv('/home/csis/codes/OpenTabulate/Libraries/vdq-lieupublic.csv')

df=df.loc[df["DESCRIPTION"]=="Bibliothèques"]

    
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

f_out='/home/csis/codes/OpenTabulate/pddir/raw/QC_QC_Libraries.csv'
df.to_csv(f_out)
