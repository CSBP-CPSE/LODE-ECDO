# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:35:10 2020

@author: josep
"""

import pandas as pd
import nltk
import re

eng=pd.read_csv(r"C:\Users\josep\Google Drive\DEIL_LODE\HealthFacilities\Metadata\Classification\NAICS 62\naics62_2017_v3-eng.csv",
                      encoding='cp1252',dtype='str')

eng['3-digit']=eng['Code'].str[0:3]

eng=eng.loc[(eng['3-digit']=='621')|(eng['3-digit']=='622')|(eng['3-digit']=='623')]

print(eng.head(20))

l621=list(eng.loc[eng['3-digit']=='621','Element Description English'])
l622=list(eng.loc[eng['3-digit']=='622','Element Description English'])
l623=list(eng.loc[eng['3-digit']=='623','Element Description English'])


s621=''
s622=''
s623=''

for el in l621:
    out = re.sub(r'[^\w\d\s]+', ' ', el)    
    s621+=out
    s621+=' '
    
for el in l622:
    out = re.sub(r'[^\w\d\s]+', ' ', el)    
    s622+=out
    s622+=' '

for el in l623:
    out = re.sub(r'[^\w\d\s]+', ' ', el)    
    s623+=out
    s623+=' '
    
L621=nltk.word_tokenize(s621)
L622=nltk.word_tokenize(s622)
L623=nltk.word_tokenize(s623)

S621=list(set(L621))
S622=list(set(L622))
S623=list(set(L623))

F621=[x for x in S621 if (x not in S622 and  x not in S623)]
F622=[x for x in S622 if (x not in S621 and  x not in S623)]
F623=[x for x in S623 if (x not in S622 and  x not in S621)]

with open('621_keywords.txt', 'w') as f:
    for item in F621:
        f.write("%s\n" % item)


with open('622_keywords.txt', 'w') as f:
    for item in F622:
        f.write("%s\n" % item)


with open('623_keywords.txt', 'w') as f:
    for item in F623:
        f.write("%s\n" % item)

