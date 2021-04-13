import pandas as pd
from postal.parser import parse_address as parse
import numpy as np
import re
from os import listdir

#note that the public school data includes lots of buildings that aren't schools, so we'll drop the entries without grade ranges
df1=pd.read_csv("/home/jovyan/data-vol-1/opentabulate/data/output/qc/PPS_Public_Immeuble_isced.csv")
df2=pd.read_csv("/home/jovyan/data-vol-1/opentabulate/data/output/qc/PPS_Prive_Installation_isced.csv")
df3=pd.read_csv("/home/jovyan/data-vol-1/opentabulate/data/output/qc/PPS_Gouvernemental_isced.csv")
df4=pd.read_csv("/home/jovyan/data-vol-1/opentabulate/data/output/qc/ES_Universitaire.csv")
df5=pd.read_csv("/home/jovyan/data-vol-1/opentabulate/data/output/qc/ES_Collegial.csv")

n1=len(df1)
df1=df1.dropna(subset=['grade_type'])
n2=len(df1)
df=pd.concat([df1,df2,df3,df4,df5])

def AddressClean(df,name_in, name_out):
	bad_list=[r'po box\b \d+',
		r'\bbox\b \d+',
		r'\bcp\b \d+',
		r'suite\b \d+',
		r'\bsuite\b \b[a-z]\b',
		r'\boffice\b \d+',
		r'\bbureau\b \d+',
		r'\bbox\b \d+',
		r'\([^()]*\)',
 		r'tel : \d{3} \d{3} \d{4}',
		r',,',
		r', +,']
	#get rid of periods
	df[name_out]=[x.replace('.','') for x in df[name_in].astype('str')]
	#make all lower case
	df[name_out]=df[name_out].str.lower()
	#replace all hyphens with a space
	df[name_out]=df[name_out].replace('-',' ',regex=True)
    #replace all commas with a space
	df[name_out]=df[name_out].replace(',',' ',regex=True)
	#delete everything in the bad list
	for expr in bad_list:

		df[name_out]=df[name_out].replace(expr,'',regex=True)
	
	#replace multiple spaces
	df[name_out]=df[name_out].replace(' +',' ',regex=True)
	#strip trailing and leading commas
	df[name_out]=df[name_out].str.strip(',')

	#strip trailing and leading spaces
	df[name_out]=df[name_out].str.strip()
	return df

df['address_str'] = df['address_str'].fillna('')
df=AddressClean(df,'address_str','address_str_clean')
#x = "#191, 1518 Centre Street N.E. Calgary AB T2E2R9"

def street_and_number(add):
    num = ''
    street = ''
    y = parse(add)
    if add != np.nan:
        for t in y:
            if "house_number" in t:
                num = t[0]
            if "road" in t:
                street = t[0]
    return num, street



ADDS=list(df.address_str_clean)
NUM=[]
STREET=[]

for a in ADDS:
    print(a)
    num, street=street_and_number(a)
    NUM.append(num)
    STREET.append(street)
    
df['street_no']=NUM
df['street_name']=STREET
print(n1-n2, 'records dropped with no grade info')
df.to_csv('qc_parsed.csv',index=False)
