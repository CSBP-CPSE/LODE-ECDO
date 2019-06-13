#This pre-processes NS libraries.
#we need to turn (lon,lat) into separate columns.

import pandas as pd

df=pd.read_csv('/home/csis/codes/OpenTabulate/Libraries/NS_Libraries.csv')


    
def strip_point(x):
	t=x.strip('(')
	t=t.rstrip(')')
#	t=t.strip(' (')
	print(t)
	return t.split()

LONGS=[]
LATS=[]
for i in df.Location:
	a=str(i)
	if a !='nan':
    
		LONGS.append(strip_point(a)[1])
		LATS.append(strip_point(a)[0])
	else:
		LONGS.append('')
		LATS.append('')
df["LONGITUDE"]=LONGS
df["LATITUDE"]=LATS

f_out='/home/csis/codes/OpenTabulate/pddir/raw/NS_Libraries.csv'
df.to_csv(f_out)