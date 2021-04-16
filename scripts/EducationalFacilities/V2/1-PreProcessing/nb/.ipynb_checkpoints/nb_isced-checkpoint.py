import pandas as pd
#note that this assumes alternative schools have no kindergarten, true in this version but maybe one day won't be
#public schools

df=pd.read_csv("NB_PublicSchools_geonb.csv",encoding='cp1252')
df=df.fillna('')

ISCED1=[]
ISCED2=[]
ISCED3=[]
print(list(df))
df['ISCED020']='0'
df.loc[(df['strGR'].str.startswith('Kindergarten'))|(df['strGR'].str.startswith('Maternelle')),'ISCED020']='1'

r=list(df['strGR'])
for k in r:
    k=k.replace('Kindergarten, ','')
    k=k.replace('Maternelle, ','')
    
    if k=='1':
        ISCED1.append('1')
        ISCED2.append('0')
        ISCED3.append('0')
    elif k=='':
        ISCED1.append('')
        ISCED2.append('')
        ISCED3.append('')
    else:

        s,e=k.split('-')
        s=s.strip()
        e=e.strip()
        print(s,e)
        if int(s)<7:
            if int(e)<7:

                ISCED1.append('1')
                ISCED2.append('0')
                ISCED3.append('0')
            elif int(e)<10:

                ISCED1.append('1')
                ISCED2.append('1')
                ISCED3.append('0')
            elif int(e)<13:

                ISCED1.append('1')
                ISCED2.append('1')
                ISCED3.append('1')
        elif int(s)<10:
            if int(e)<10:

                ISCED1.append('0')
                ISCED2.append('1')
                ISCED3.append('0')
            elif int(e)<13:

                ISCED1.append('0')
                ISCED2.append('1')
                ISCED3.append('1')
        else:

                ISCED1.append('0')
                ISCED2.append('0')
                ISCED3.append('1')

           
df['ISCED1']=ISCED1
df['ISCED2']=ISCED2
df['ISCED3']=ISCED3

df.to_csv("NB_PublicSchools_geonb_isced.csv",encoding='cp1252',index=False)

#First Nations Schools
df=pd.read_csv("NB_FirstNationsSchools.csv",encoding='cp1252')
df=df.fillna('')

ISCED1=[]
ISCED2=[]
ISCED3=[]
print(list(df))
df['ISCED020']='0'
df.loc[(df['Grade'].str.startswith('Kindergarten')),'ISCED020']='1'

r=list(df['Grade'])
for k in r:
    k=k.replace('Kindergarten, K4, ','')
    
    if k=='1':
        ISCED1.append('1')
        ISCED2.append('0')
        ISCED3.append('0')
    elif k=='':
        ISCED1.append('')
        ISCED2.append('')
        ISCED3.append('')
    else:
        
        s,e=k.split('--')
        s=s.strip()
        e=e.strip()
        print(s,e)
        if int(s)<7:
            if int(e)<7:

                ISCED1.append('1')
                ISCED2.append('0')
                ISCED3.append('0')
            elif int(e)<10:

                ISCED1.append('1')
                ISCED2.append('1')
                ISCED3.append('0')
            elif int(e)<13:

                ISCED1.append('1')
                ISCED2.append('1')
                ISCED3.append('1')
        elif int(s)<10:
            if int(e)<10:

                ISCED1.append('0')
                ISCED2.append('1')
                ISCED3.append('0')
            elif int(e)<13:

                ISCED1.append('0')
                ISCED2.append('1')
                ISCED3.append('1')
        elif int(s)<13:

                ISCED1.append('0')
                ISCED2.append('0')
                ISCED3.append('1')
            

           
df['ISCED1']=ISCED1
df['ISCED2']=ISCED2
df['ISCED3']=ISCED3

df.to_csv("NB_FirstNationsSchools_isced.csv",encoding='cp1252', index=False)

#alternative learning centre


df=pd.read_csv("NB_AlternativeLearningCentre.csv",encoding='cp1252')

ISCED1=[]
ISCED2=[]
ISCED3=[]
print(list(df))
df=df.fillna('')
r=list(df['Grade'])
for k in r:
    k=k.replace('Kindergarten, K4, ','')
    
    if k=='1':
        ISCED1.append('1')
        ISCED2.append('0')
        ISCED3.append('0')
    elif k=='':
        ISCED1.append('')
        ISCED2.append('')
        ISCED3.append('')
    else:
        
        s,e=k.split('--')
        s=s.strip()
        e=e.strip()
        print(s,e)
        if int(s)<7:
            if int(e)<7:

                ISCED1.append('1')
                ISCED2.append('0')
                ISCED3.append('0')
            elif int(e)<10:

                ISCED1.append('1')
                ISCED2.append('1')
                ISCED3.append('0')
            elif int(e)<13:

                ISCED1.append('1')
                ISCED2.append('1')
                ISCED3.append('1')
        elif int(s)<10:
            if int(e)<10:

                ISCED1.append('0')
                ISCED2.append('1')
                ISCED3.append('0')
            elif int(e)<13:

                ISCED1.append('0')
                ISCED2.append('1')
                ISCED3.append('1')
        elif int(s)<13:

                ISCED1.append('0')
                ISCED2.append('0')
                ISCED3.append('1')
        else:
                ISCED1.append('')
                ISCED2.append('')
                ISCED3.append('')
            
#There are no kindergarten schools in this data, can set ISCED020 to 0
df['ISCED020']='0'
df['ISCED1']=ISCED1
df['ISCED2']=ISCED2
df['ISCED3']=ISCED3

df.to_csv("NB_AlternativeLearningCentre_isced.csv",encoding='cp1252', index=False)


