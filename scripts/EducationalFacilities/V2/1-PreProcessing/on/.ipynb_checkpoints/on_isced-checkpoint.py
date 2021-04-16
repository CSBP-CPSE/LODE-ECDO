import pandas as pd

#public schools

df=pd.read_csv("new_sif_data_table_2018_2019prelim_en_september.csv",encoding='cp1252')

for i in df['Grade Range'].unique():
    print(i)
    
ISCED010=[]
ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]
print(list(df))


r=list(df['Grade Range'])
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
        elif s=='K':
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

df.to_csv("new_sif_data_table_2018_2019prelim_en_september_isced.csv",encoding='cp1252',index=False)

#for private schools
#Ministry of Education documents divide grades into two categories: Elementary (Grades 1–8) and Secondary (Grades 9–12). (wikipedia)
#this means elementary maps to ISCED1 and ISCED2, and secondary maps to ISCED2 and ISCED3.
df=pd.read_csv("on_private_schools_contact_information_october_2020_en.csv",encoding='cp1252')

for i in df['School Level'].unique():
    print(i)

df['ISCED1']=''
df['ISCED2']=''
df['ISCED3']=''
df['ISCED020']='0'
df['ISCED010']='0'

df.loc[(df['School Level']=='Elementary')|(df['School Level']=='Elem/Sec'),'ISCED1']='1'
df.loc[(df['School Level']=='Elementary')|(df['School Level']=='Elem/Sec'),'ISCED2']='1'
df.loc[(df['School Level']=='Elementary'),'ISCED3']='0'

df.loc[(df['School Level']=='Secondary')|(df['School Level']=='Elem/Sec'),'ISCED2']='1'
df.loc[(df['School Level']=='Secondary')|(df['School Level']=='Elem/Sec'),'ISCED3']='1'
df.loc[(df['School Level']=='Secondary'),'ISCED1']='0'


df.to_csv("on_private_schools_contact_information_october_2020_en_isced.csv",encoding='cp1252',index=False)
