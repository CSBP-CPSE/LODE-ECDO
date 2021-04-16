import pandas as pd

df=pd.read_csv("NT-education.csv",encoding='cp1252')

# some grade ranges were converted, probably by excel, to dates

fixes={'12-Jul':'7-12',
'12-Aug':'8-12', 
'07-Apr' :'4-7',
'07-Jun':'6-7'
}

for key, value in fixes.items():
    df.GRADE=df.GRADE.str.replace(key,value)
print(df.GRADE.unique())


ISCED010=[]
ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]
print(list(df))


r=list(df['GRADE'])
for k in r:

    if k=='':
        ISCED1.append('')
        ISCED2.append('')
        ISCED3.append('')
    else:

        s,e=k.split('-')
        s=s.strip()
        e=e.strip()
        print(s,e)
        if s=='JK':
            if int(e)<7:
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

df.to_csv("NT-education_isced.csv",encoding='cp1252',index=False)