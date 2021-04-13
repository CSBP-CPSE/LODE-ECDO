import pandas as pd

df=pd.read_csv('nl_allschools1920.csv')

ISCED020=[]
ISCED1=[]
ISCED2=[]
ISCED3=[]

def is_greater_than_0(x):
    if x>0:
        return 1
    else:
        return 0
    
df['ISCED020']=df['k'].apply(is_greater_than_0)

print(df[['k','ISCED020']])

df['1_to_6']=df['one']	+df['two']	+df['three']	+df['four']	+df['five']	+df['six']
df['7_to_9']=df['seven']	+df['eight']	+df['nine']
df['10_to_12']=df['ten']	+df['eleven']	+df['twelve']

df['ISCED1']=df['1_to_6'].apply(is_greater_than_0)
df['ISCED2']=df['7_to_9'].apply(is_greater_than_0)
df['ISCED3']=df['10_to_12'].apply(is_greater_than_0)

df.to_csv('nl_allschools1920_isced.csv',index=False)

