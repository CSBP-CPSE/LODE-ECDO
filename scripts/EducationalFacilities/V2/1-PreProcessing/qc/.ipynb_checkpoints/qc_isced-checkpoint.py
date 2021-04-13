import pandas as pd

#public
"""
The public schools file also contains quite a few entries (over a thousand) with names like "Duplex" and with no grade information
These seem to be buildings owned by public school entities, but that are not schools themselves. 
These are dropped here.
"""

df=pd.read_csv("PPS_Public_Immeuble.csv", delimiter=';')

df['ISCED020'] = ''
df['ISCED1'] = ''
df['ISCED2'] = ''
df['ISCED3'] = ''
df['ISCED4+'] = ''

df.loc[df.PRESC==1,'ISCED020']='1'
df.loc[df.PRIM==1,'ISCED1']='1'
df.loc[df.SEC==1,'ISCED2']='1'
df.loc[df.SEC==1,'ISCED3']='1'
df.loc[df.FORM_PRO==1,'ISCED4+']='1'
df.loc[df.PRESC==0,'ISCED020']='0'
df.loc[df.PRIM==0,'ISCED1']='0'
df.loc[df.SEC==0,'ISCED2']='0'
df.loc[df.SEC==0,'ISCED3']='0'
df.loc[df.FORM_PRO==0,'ISCED4+']='0'
print(len(df))
df=df.loc[~df.STYLE_CART.str.startswith("5_Imm")]
print(len(df))
df.to_csv("PPS_Public_Immeuble_isced.csv",index=False)

#private

df=pd.read_csv("PPS_Prive_Installation.csv", delimiter=';')

df['ISCED020'] = ''
df['ISCED1'] = ''
df['ISCED2'] = ''
df['ISCED3'] = ''
df['ISCED4+'] = ''

df.loc[df.PRESC==1,'ISCED020']='1'
df.loc[df.PRIM==1,'ISCED1']='1'
df.loc[df.SEC==1,'ISCED2']='1'
df.loc[df.SEC==1,'ISCED3']='1'
df.loc[df.FORM_PRO==1,'ISCED4+']='1'
df.loc[df.PRESC==0,'ISCED020']='0'
df.loc[df.PRIM==0,'ISCED1']='0'
df.loc[df.SEC==0,'ISCED2']='0'
df.loc[df.SEC==0,'ISCED3']='0'
df.loc[df.FORM_PRO==0,'ISCED4+']='0'

df.to_csv("PPS_Prive_Installation_isced.csv",index=False)

#gouvernemantal

df=pd.read_csv("PPS_Gouvernemental.csv", delimiter=';')

df['ISCED020'] = ''
df['ISCED1'] = ''
df['ISCED2'] = ''
df['ISCED3'] = ''
df['ISCED4+'] = ''


df.loc[df.PRESC==1,'ISCED020']='1'
df.loc[df.PRIM==1,'ISCED1']='1'
df.loc[df.SEC==1,'ISCED2']='1'
df.loc[df.SEC==1,'ISCED3']='1'
df.loc[df.FORM_PRO==1,'ISCED4+']='1'

df.loc[df.PRESC==0,'ISCED020']='0'
df.loc[df.PRIM==0,'ISCED1']='0'
df.loc[df.SEC==0,'ISCED2']='0'
df.loc[df.SEC==0,'ISCED3']='0'
df.loc[df.FORM_PRO==0,'ISCED4+']='0'

df.to_csv("PPS_Gouvernemental_isced.csv",index=False)