#preprocessing for Sherbrooke
# turn Point into long and lat, export csv
#includes repeated entries for different days, (hours)
#limit ourselves to wednesday entries (all libraries have wed. hours)
#There are errors in postal codes, so we're not including them
import pandas as pd

#read shapefile with geopandas into geodataframe
df=pd.read_csv('/home/csis/codes/OpenTabulate/Libraries/QC_Sherbrooke_Libraries.csv',encoding="iso-8859-1", delimiter='|')
#print(list(df))
#limit to Wednesday schedule entries
df=df.loc[df["HOR"]=="Mercredi"]
def strip_point(x):
	t=x.strip('POINT(')
	t=t.rstrip(')')
	#print(t.split('-'))
	return t.split('-')

LONGS=[]
LATS=[]

for i in df.GEOM:
	a=str(i)
	print(strip_point(a))
	b=strip_point(a)
	LONGS.append('-'+b[1])
	LATS.append(b[0])
    
df["LONGITUDE"]=LONGS
df["LATITUDE"]=LATS    

#POSTAL_CODES=[]
#for i in df["AD"]:
#    POSTAL_CODES.append(i[-7:])
#df["POSTAL_CODES"]=POSTAL_CODES
df.to_csv('/home/csis/codes/OpenTabulate/pddir/raw/QC_Sherbrooke_Libraries.csv')
