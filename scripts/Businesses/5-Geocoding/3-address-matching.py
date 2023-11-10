# This finds address matches between files by looking for exact matches on street number and 'fuzzy' matches on street name
# the goal is to use Open Addresses files to assign geocoordinates

# I want to start by trying out the script on a sample. 
# download ODA data for Alberta.

# conda install thefuzz
# conda install unidecode

import pandas as pd

from thefuzz import fuzz
from thefuzz import process
import time
import sys
import unidecode #to remove accents
import re
from AddressFuncs import DirectionCheck, NameIsNumber
import sys


# input_dir='inputs/'
# output_dir='outputs/'

# inputs 
# formatted_on_test.csv
# ODA_MB_v1.csv

# database=sys.argv[1]
# addresses=sys.argv[2]
# output=sys.argv[3]

# t1=time.time()


#This is a semi-arbitrary cut off for fuzzy string matching
cut_off=70
#Read input files

# loop through and do seperately for each province 
# let's test it on one province again first. AB


provinces = ['AB', 'BC', 'MB', 'NB', 'NT', 'NS', 'ON', 'PE', 'QC', 'SK']
# provinces = ['AB', 'BC', 'MB']

# for province_code in provinces:
#     file_location = "https://www150.statcan.gc.ca/n1/pub/46-26-0001/2021001/ODA_" + province_code + "_v1.zip"

# for each province, subset the correct bit of formatted for df
# get the correct file for DF
# save it to a unique file name

df_all = pd. DataFrame()

for province_code in provinces:
    
    t1=time.time()
    
    print(province_code)

    # df=pd.read_csv(input_dir+database)
    df = pd.read_csv('formatted.csv', low_memory=False)

    # test 
    df = df[df['province'] == province_code]

    # drop any entries without a street number
    df = df.dropna(subset=['street_no'])
    
    print('rows: ', len(df))

    #read in openadress file
    # DF=pd.read_csv(input_dir+addresses)
    
    ocd_file = "data/oda-addresses/ODA_" + province_code + "_v1.csv"

    DF=pd.read_csv(ocd_file, low_memory=False)
    #drop any entries without a street number
    DF=DF.dropna(subset=['street_no'])
    
    

    # SAM need to adjust to use formatted street names
    # formatted_en

    #force street numbers to be integers then strings (pandas converts to float if there are empty entries)
    df["street_no"] = df["street_no"].astype('int', errors='ignore').astype('str')
    DF["street_no"] = DF["street_no"].astype('int', errors='ignore').astype('str')

    # FOR TESTING, remove duplicates

    d1 = len(df)
    df = df.drop_duplicates(subset=['street_no','formatted_en'])
    d2 = len(df)
    
    print('rows after deduplication: ', d2)
    ######
    
    print('ODA addresses:', len(DF))
    
    # FOR TESTING take a sample
    if (len(df) > 100):
        df = df.sample(100)


    num=list(df["street_no"])
    street=[]
    
    
    #remove accents from input dataframe
    
    if (province_code == 'QC'):
        for i in df.formatted_fr.astype('str'):
            street.append(unidecode.unidecode(i))
    else:
        for i in df.formatted_en.astype('str'):
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
        DF_temp=DF.loc[DF["street_no"]==number]

        #remove accents from address database, and restrict to unique names (avoid repetitions)
        STREET=[]
        for j in DF_temp["street"].unique().astype('str'):
            STREET.append(unidecode.unidecode(j))	



        #process reduced address list with fuzzywuzzy


        addr1=street[i]
        if STREET==[]: #this means the street number isn't in the address list, so obviously no match
            #do nothing
            r=0
            best=''
        else:		
            bests=process.extract(addr1,STREET,scorer=fuzz.ratio)
    # 		print(bests)
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
                x[i]=DF_temp.loc[DF_temp["street"]==best,"longitude"].mean()
                y[i]=DF_temp.loc[DF_temp["street"]==best,"latitude"].mean()
        else:
                x[i]=''
                y[i]=''
    df["matches_r"]=MATCHES_r	
    df["ratio"]=ratio


    df["x"]=x
    df["y"]=y

    #create output
    # for testing, we don't need all the columns - just the address, and maybe the name
#     cols = list(df)
    # df_out = df[[cols[0],'street_no','street_name','matches_r','ratio','x','y']]
    
    no_matches = df['ratio'][df['ratio'] > cut_off].count()
    print('percent matches (from sample n = 100): ', no_matches)
    
    output_filename = 'output-' + province_code + '.csv'
    df.to_csv(output_filename, index=False)

    t2=time.time()
    print('time taken: ', str(round(t2-t1, 2)), '\n')
    
    df_all = df_all.append(df)
    

df_all.to_csv("output_all.csv", index=False)