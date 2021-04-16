import pandas as pd

df=pd.read_csv("Schools in MB Jan 2019.csv", encoding="cp1252")

ISCED010=[]
ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]

r=list(df.gradeString)
for k in r:
    s,e=k.split('-')
    s=s.strip()
    e=e.strip()
    print(s,e)
    if s=='N':
        if (e=='M' or e=='K'):
            ISCED010.append('1')
            ISCED020.append('1')
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
        
    elif (s=='M' or s=='K'):
        if (e=='M' or e=='K'):
            ISCED010.append('0')
            ISCED020.append('1')
            ISCED1.append('0')
            ISCED2.append('0')
            ISCED3.append('0')
        elif int(e)<7:
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

df.to_csv("Schools in MB Jan 2019_isced.csv", encoding='cp1252',index=False)