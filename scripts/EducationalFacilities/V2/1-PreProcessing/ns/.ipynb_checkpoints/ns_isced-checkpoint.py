import pandas as pd
"""
Note that Nova Scotia has a year Primary before first grade, which in this case maps to kindergarten/ISCED020. 
Pre-Primary is mapped to to ISCED010.
https://novascotiaimmigration.com/live-here/education/
"""
#public
df=pd.read_csv('directoryofpublicschools2019-2020.csv',encoding='cp1252')
ISCED010=[]
ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]

START=list(df['Start Gr'])
END=list(df['End Gr'])
for i in range(len(START)):
    
    s=START[i]
    e=END[i]
    print(s,e)
    if s=='PP':
        if (e=='PP' or e=='PP'):
            ISCED010.append('1')

            ISCED020.append('0')
            ISCED1.append('0')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<7:
            ISCED010.append('1')

            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<10:
            ISCED010.append('1')
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('0')
        elif int(e)<13:
            ISCED010.append('1')
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('1')
        
    elif s=='PR':
        if int(e)<7:
            ISCED010.append('0')
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<10:
            ISCED010.append('0')
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('0')
        elif int(e)<13:
            ISCED010.append('0')
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('1')
    
    elif int(s)<7:
        if int(e)<7:
            ISCED010.append('0')
            ISCED020.append('0')
            ISCED1.append('1')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<10:
            ISCED010.append('0')
            ISCED020.append('0')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('0')
        elif int(e)<13:
            ISCED010.append('0')
            ISCED020.append('0')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('1')
    elif int(s)<10:
        if int(e)<10:
            ISCED010.append('0')
            ISCED020.append('0')
            ISCED1.append('0')
            ISCED2.append('1')
            ISCED3.append('0')
        elif int(e)<13:
            ISCED010.append('0')
            ISCED020.append('0')
            ISCED1.append('0')
            ISCED2.append('1')
            ISCED3.append('1')
    else:
            ISCED010.append('0')
            ISCED020.append('0')
            ISCED1.append('0')
            ISCED2.append('0')
            ISCED3.append('1')
            
df['ISCED010']=ISCED010
df['ISCED020']=ISCED020            
df['ISCED1']=ISCED1
df['ISCED2']=ISCED2
df['ISCED3']=ISCED3


df.to_csv('directoryofpublicschools2019-2020_isced.csv',encoding='cp1252',index=False)


#private

df=pd.read_csv("Recognized_Private_Schools_Granting_the_Nova_Scotia_High_School_Leaving_Certificate.csv")

for i in df['Grade Level'].unique():
    print(i)

df['Grade Level']=df['Grade Level'].str.replace('2019-07-12T00:00:00.000','7-12')

ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]

r=list(df['Grade Level'])
for k in r:
    k=k.replace('Gr','')
    s,e=k.split('-')
    s=s.strip()
    e=e.strip()
    print(s,e)
 
    if (s=='P'):
        if (e=='P' or e=='K'):
            ISCED020.append('1')
            ISCED1.append('0')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<7:
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<10:
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('0')
        elif int(e)<13:
            ISCED020.append('1')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('1')
    
    elif int(s)<7:
        if int(e)<7:
            ISCED020.append('0')
            ISCED1.append('1')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<10:
            ISCED020.append('0')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('0')
        elif int(e)<13:
            ISCED020.append('0')
            ISCED1.append('1')
            ISCED2.append('1')
            ISCED3.append('1')
    elif int(s)<10:
        if int(e)<10:
            ISCED020.append('0')
            ISCED1.append('0')
            ISCED2.append('1')
            ISCED3.append('0')
        elif int(e)<13:
            ISCED020.append('0')
            ISCED1.append('0')
            ISCED2.append('1')
            ISCED3.append('1')
    else:
            ISCED020.append('0')
            ISCED1.append('0')
            ISCED2.append('0')
            ISCED3.append('1')
            
df['ISCED020']=ISCED020            
df['ISCED1']=ISCED1
df['ISCED2']=ISCED2
df['ISCED3']=ISCED3

df.to_csv("Recognized_Private_Schools_Granting_the_Nova_Scotia_High_School_Leaving_Certificate_isced.csv")
