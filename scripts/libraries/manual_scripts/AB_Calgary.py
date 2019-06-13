#This pre-processes Calgary libraries.
#we need to turn (lon,lat) into separate columns.

import pandas as pd
import re

df=pd.read_csv('/home/csis/codes/OpenTabulate/Libraries/AB_Calgary_Libraries.csv')


    
def strip_point(x):
	t=x.strip('(')
	t=t.rstrip(')')
#	t=t.strip(' (')
#	print(t)
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

ADD2=[]
for i in df.Address:
	a=str(i)
	b=re.sub("\n(.*)","",a)
	ADD2.append(b)
#	print(b)
df.Address=ADD2
f_out='/home/csis/codes/OpenTabulate/pddir/raw/AB_Calgary_Libraries.csv'
df.to_csv(f_out)
