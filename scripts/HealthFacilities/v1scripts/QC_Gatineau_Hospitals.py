import pandas as pd

df=pd.read_csv('/home/csis/codes/OpenTabulate/pddir/raw/Gatineau_QC_Hospitals.csv', encoding='iso-8859-1')

def strip_point(x):
	t=x.strip('POINT (')
	t=t.rstrip(')')
#	t=t.strip(' (')
	print(t)
	return t.split()

LONGS=[]
LATS=[]
for i in df.GEOM:
	LONGS.append(strip_point(i)[0])
	LATS.append(strip_point(i)[1])

df["LONGITUDE"]=LONGS
df["LATITUDE"]=LATS

df.to_csv('Gatineau_QC_Hospitals.csv')
