import pandas as pd
import requests
import os
import datetime

df = pd.read_csv("Open_Sources.csv")

#print list(df)

Prov=df.Province
City=df["City or Region"]
Links=df["Source"]
AS=df["Attribution Statement"]
License=df["License or Terms of Use"]
IsOpen=df.Open
#Make directories and download sources

for i in range(len(Prov)):
    dirname=Prov[i]+'/'+City[i]
    if IsOpen[i]=='Open': #Only get open sources
        try:
            os.makedirs(dirname)    
            print("Directory " , dirname ,  " Created ")
        except: 
            print("Directory " , dirname ,  " already exists")  
            continue

date=datetime.datetime.today().strftime('%Y-%m-%d')
#Download sources and create README files
        
for i in range(len(Prov)):
    dirname=Prov[i]+'/'+City[i]
    if IsOpen[i]=='Open': #Only get open sources

        f=requests.get(Links[i])
        g=open(dirname+'/GTFS.zip','wb')
        g.write(f.content)
        g.close()
        RM=open(dirname+'/README.txt','w')
        RM.write(AS[i]+'\n')
        RM.write('License: '+License[i]+'\n')
        RM.write('Downloaded on '+date)
        RM.close()
    