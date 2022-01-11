import pandas as pd

f_in = ""
f_out = ""
df=pd.read_csv(f_in, low_memory=False, dtype='str')
#merge parsed columns with other columns

df['street_no'] = df['street_no'].fillna(df['LP_street_no'])
df['street_name'] = df['street_name'].fillna(df['LP_street_name'])
df['postal_code'] = df['postal_code'].fillna(df['LP_PostCode'].str.upper())
df['city'] = df['city'].fillna(df['LP_City'].str.capitalize())
df['unit'] = df["LP_Unit"].str.capitalize()

f_out = df.to_csv(f_out, index=False)