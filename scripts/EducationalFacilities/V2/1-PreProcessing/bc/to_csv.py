"""
The BC grade range system is fairly complex to parse because in addition to grades, it has K, pre-K, and SU, EU, and GA.
EU: Elementary Ungraded, map to ISCED1 and ISCED2 (because elementary in BC is 1 to 7 and ISCED2 is 7-9)
SU: Secondary Ungraded, map to ISCED2 and ISCED3
GA: Graduated Adult, map to nothing

"""

import pandas as pd

df=pd.read_excel('excelSchoolContact.xls')

ISCED010=[]
ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]




r=list(df["Grade Range"])
for k in r:
    if k=='No Enrolment Reported':
        ISCED010.append('')
        ISCED020.append('')
        ISCED1.append('')
        ISCED2.append('')
        ISCED3.append('')
    elif k == 'Pre-K':
        ISCED010.append('1')
        ISCED020.append('0')
        ISCED1.append('0')
        ISCED2.append('0')
        ISCED3.append('0')
    elif k == "GA":
        ISCED010.append('')
        ISCED020.append('')
        ISCED1.append('')
        ISCED2.append('')
        ISCED3.append('')
    elif k == "EU":
        ISCED010.append('0')
        ISCED020.append('0')
        ISCED1.append('1')
        ISCED2.append('1')
        ISCED3.append('0')    
    elif k == "SU":
        ISCED010.append('0')
        ISCED020.append('0')
        ISCED1.append('0')
        ISCED2.append('1')
        ISCED3.append('1')    
    elif k == 'K':
        ISCED010.append('0')
        ISCED020.append('1')
        ISCED1.append('0')
        ISCED2.append('0')
        ISCED3.append('0')
    else:

        T=k.split(',') #check to see if it's multiple things separated by a comma
      
        t=T[0]
        if '-' not in t: #just a number on its own, no range
            if t=='K':
                ISCED010.append('0')
                ISCED020.append('1')
                ISCED1.append('0')
                ISCED2.append('0')
                ISCED3.append('0')
            elif int(t)<7:
                ISCED010.append('0')
                ISCED020.append('0')
                ISCED1.append('1')
                ISCED2.append('0')
                ISCED3.append('0')
            elif int(t)<10:
                ISCED010.append('0')
                ISCED020.append('0')
                ISCED1.append('0')
                ISCED2.append('1')
                ISCED3.append('0')
            elif int(t)>=10:
                ISCED010.append('0')
                ISCED020.append('0')
                ISCED1.append('0')
                ISCED2.append('0')
                ISCED3.append('1')
        else: #this means it's a grade range
            s,e=t.split('-')
            s=s.strip()
            e=e.strip()
            if s=='K':
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
            else:
                if int(s)< 7 and int(e)<7:
                    ISCED010.append('0')
                    ISCED020.append('0')
                    ISCED1.append('1')
                    ISCED2.append('0')
                    ISCED3.append('0')
                elif int(s)<7 and int(e)<10:
                    ISCED010.append('0')
                    ISCED020.append('0')
                    ISCED1.append('1')
                    ISCED2.append('1')
                    ISCED3.append('0')
                elif int(s)<7 and int(e)<13:
                    ISCED010.append('0')
                    ISCED020.append('0')
                    ISCED1.append('1')
                    ISCED2.append('1')
                    ISCED3.append('1')
                elif int(s)< 10 and int(e)<10:
                    ISCED010.append('0')
                    ISCED020.append('0')
                    ISCED1.append('0')
                    ISCED2.append('1')
                    ISCED3.append('0')
                elif int(s)<10 and int(e)<13:
                    ISCED010.append('0')
                    ISCED020.append('0')
                    ISCED1.append('0')
                    ISCED2.append('1')
                    ISCED3.append('1')
                elif int(s)<13 and int(e)<13:
                    ISCED010.append('0')
                    ISCED020.append('0')
                    ISCED1.append('0')
                    ISCED2.append('0')
                    ISCED3.append('1')
        
                    
print(len(ISCED010))
                
df['ISCED010']=ISCED010
df['ISCED020']=ISCED020            
df['ISCED1']=ISCED1
df['ISCED2']=ISCED2
df['ISCED3']=ISCED3

#now we will deal with the rest of the SU and EU

df.loc[df['Grade Range'].str.contains('SU'),'ISCED2'] = '1'
df.loc[df['Grade Range'].str.contains('SU'),'ISCED3'] = '1'
df.loc[df['Grade Range'].str.contains('EU'),'ISCED1'] = '1'
df.loc[df['Grade Range'].str.contains('EU'),'ISCED2'] = '1'


df.to_csv('excelSchoolContact_isced.csv',index=False)