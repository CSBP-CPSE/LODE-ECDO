#Processing PEI health centre locations
#Strip out nursing homes, and turn 'Location" column into long and lat
import pandas as pd

df=pd.read_csv('/home/csis/codes/OpenTabulate/pddir/raw/PE_Hospitals.csv')

df=df.loc[df["Facility Type"] != "Public Nursing Home"]
def strip_point(x):
	t=x.strip('(')
	t=t.rstrip(')')
#	t=t.strip(' (')
	print(t)
	return t.split()

LONGS=[]
LATS=[]
for i in df["Location 1"]:
	LONGS.append(strip_point(i)[1])
	LATS.append(strip_point(i)[0])

df["LONGITUDE"]=LONGS
df["LATITUDE"]=LATS

df.to_csv('/home/csis/codes/OpenTabulate/pddir/raw/PE_Hospitals.csv')
