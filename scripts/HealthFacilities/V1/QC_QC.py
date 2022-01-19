#PReprocessing for QC_QC
#This data was already extracted from a csv of public buildings by limiting to type "hopitaux"
#This converts geometry column to lat and lon
import pandas as pd

df=pd.read_csv('/home/csis/codes/OpenTabulate/pddir/raw/QC_QC_Hospitals.csv', encoding='iso-8859-1')

def strip_point(x):
	t=x.strip('POINT (')
	t=t.rstrip(')')
	print(t)
	return t.split()

LONGS=[]
LATS=[]
for i in df.GEOMETRIE:
	LONGS.append(strip_point(i)[0])
	LATS.append(strip_point(i)[1])

df["LONGITUDE"]=LONGS
df["LATITUDE"]=LATS

df.to_csv('QC_QC_Hospitals.csv')
