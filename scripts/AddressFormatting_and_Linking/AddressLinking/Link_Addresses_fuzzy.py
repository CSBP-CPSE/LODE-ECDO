
#This finds address matches between files by looking for exact matches on street number and 'fuzzy' matches on street name
#the goal is to use Open Addresses files to assign geocoordinates

import pandas as pd

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
import sys
import unidecode #to remove accents
import re
from AddressFuncs import DirectionCheck, NameIsNumber
import sys

input_dir='data/TESTING/inputs/'
output_dir='data/TESTING/outputs/'

database=sys.argv[1]
addresses=sys.argv[2]
output=sys.argv[3]


t1=time.time()


#This is a semi-arbitrary cut off for fuzzy string matching
cut_off=70
#Read input files


df=pd.read_csv(input_dir+database)

#drop any entries without a street number
df=df.dropna(subset=['street_no'])

#read in openadress file
DF=pd.read_csv(input_dir+addresses)
#drop any entries without a street number
DF=DF.dropna(subset=['NUMBER'])

#force street numbers to be integers then strings (pandas converts to float if there are empty entries)
df["street_no"]=df["street_no"].astype('int', errors='ignore').astype('str')
DF["NUMBER"]=DF["NUMBER"].astype('int', errors='ignore').astype('str')

#FOR TESTING, remove duplicates

df=df.drop_duplicates(subset=['street_no','street_name'])
######

num=list(df["street_no"])
street=[]

#remove accents from input dataframe
for i in df.street_name.astype('str'):
	street.append(unidecode.unidecode(i))

n=len(num)
MATCHES_r=[0]*n

ratio=[0]*n

x=[0]*n
y=[0]*n




#loop through main list
for i in range(n):
	number=num[i]

	#restrict to only consider entries with a matching street number
	DF_temp=DF.loc[DF["NUMBER"]==number]

	#remove accents from address database, and restrict to unique names (avoid repetitions)
	STREET=[]
	for j in DF_temp["STREET"].unique().astype('str'):
		STREET.append(unidecode.unidecode(j))	



	#process reduced address list with fuzzywuzzy


	addr1=street[i]
	if STREET==[]: #this means the street number isn't in the address list, so obviously no match
		#do nothing
		r=0
		best=''
	else:		
		bests=process.extract(addr1,STREET,scorer=fuzz.ratio)
		print(bests)
		#The print statement below is to determine how much 'better' the best match is than the 2nd best
#		if len(bests)>1:	
#			print((bests[0])[1]-(bests[1])[1])

		#bests is a list of tuples, of the form ("street name", ratio) 
		b0=bests[0]
	
		r=b0[1]
		best=b0[0]
		ratio[i]=r
		MATCHES_r[i]=best
	#This is where we determine if we found an address match
	#We consider a match if the 'best' match is significantly better than the 2nd best, AND that the best is also good (>70, semi-arbitrary cut-off).
		#assume directions match until we find they don't
		DIR_MATCH=True
		RAT_MATCH=False
		if r>cut_off:
			if r==100: #perfect string match
				RAT_MATCH=True
			else:
				check_list=pd.Series([addr1,best])						
				#check to see if direction exists and matches
				DIR_MATCH=DirectionCheck(check_list)
				#check to see if the street name is a number and that if so it isn't a mismatch
				NUM_MATCH=NameIsNumber(check_list)
				if (DIR_MATCH==True) and (NUM_MATCH==True):
					if len(bests)>1:
						r1=(bests[1])[1]
						if (r-r1)>10: #clearly better than 2nd option
							RAT_MATCH=True

					
						else: #not clearly better than second option
							RAT_MATCH=False

					
					else: #Only one option, and score above 70
						RAT_MATCH=True
				else:
					RAT_MATCH =False
		else: #Best option ratio <cutoff, not good
			RAT_MATCH=False
			
		
	if RAT_MATCH==True:
			#some addresses repeat in address lists with slightly different lat/lons
			#this is PERPLEXING. We take the mean.
			x[i]=DF_temp.loc[DF_temp["STREET"]==best,"LON"].mean()
			y[i]=DF_temp.loc[DF_temp["STREET"]==best,"LAT"].mean()
	else:
			x[i]=''
			y[i]=''
df["matches_r"]=MATCHES_r	
df["ratio"]=ratio


df["x"]=x
df["y"]=y

#################create output
#for testing, we don't need all the columns - just the address, and maybe the name
cols=list(df)
df_out=df[[cols[0],'street_no','street_name','matches_r','ratio','x','y']]

df_out.to_csv(output_dir+output,index=False)

t2=time.time()
print('time ', t2-t1)

