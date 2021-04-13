import pandas as pd

df=pd.read_csv('yt-education-2.csv')

ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]

r=list(df['grades'])
for k in r:
    s,e=k.split('to')
    s=s.strip()
    e=e.strip()
    print(s,e)
 
    if (s=='k' or s=='K'):
        if (e=='k' or e=='K'):
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

df.to_csv('yt-education-2_isced.csv',index=False)
