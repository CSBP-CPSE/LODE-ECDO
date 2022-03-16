"""
Bruno from SGC previously geocoded the alpha version, and then geocoded the update to the ESDC facilities. 
This script takes the latest merged version of the ODEF, and joins it on the previous geocoded files to assign coordinates.
"""

import pandas as pd

geo1 = pd.read_csv("inputs/ODEFv2_alpha_18-11-2020-geocoded.csv", low_memory=False, dtype="str")
geo2 = pd.read_csv("inputs/ESDC_Designated_Institutions_geocoded.csv", low_memory=False, dtype="str")

df = pd.read_csv("../4-Parsing/ODEFv2_26-03-2021-parsed.csv", encoding="utf-8", dtype="str", low_memory=False)


#split dataframe into entries that have coordinates already, and those that don't.
df_nulls= df.copy()
df_nulls=df_nulls.loc[df_nulls.latitude.isnull()]

df_filled=df.copy()
df_filled=df_filled.loc[~df_filled.latitude.isnull()]
print(len(df_filled))
#reduce geo1 and geo2 to needed columns, and drop ESDC from geo1 since it's been replaced

geo1 = geo1.loc[geo1.provider!="Employment and Social Development Canada"]

print(list(geo1))
geo1 = geo1[['source_id', 'facility_name', 'address_str','street_no', 'street_name', 'street_addr', 'city', 'postal_code', 'provider',  'Score', 'Addr_type', 'street_X', 'street_Y']]
geo2 = geo2[['Score', 'Addr_type', "X", "Y", "USER_source_id"]]

#merge on ESDC first, it's easier

df1 = pd.merge(df_nulls, geo2, how="left", left_on="source_id", right_on="USER_source_id")
print(len(df_nulls), len(df1))

df1 = pd.merge(df1, geo1, how="left", on=["provider", "facility_name", "address_str", "city"], suffixes=('','_y'))

df1["X"] = df1["X"].fillna(df1["street_X"])
df1["Y"] = df1["Y"].fillna(df1["street_Y"])
df1["Score"] = df1["Score"].fillna(df1["Score_y"])
df1["Addr_type"] = df1["Addr_type"].fillna(df1["Addr_type_y"])

DF=pd.concat([df_filled, df1], ignore_index=True)
print(len(DF))


#drop no longer needed columns

to_drop=['USER_source_id', 'street_X', 'street_Y']
for i in list(DF):
    if i.endswith("_y"):
        to_drop.append(i)
DF=DF.drop(columns=to_drop)

types=['PointAddress', 'Subaddress', 'POI', 'StreetAddress', 'StreetAddressExt',
       'StreetInt']

scores=list(DF.Score)
Addr_type=list(DF.Addr_type)
Lats=list(DF.latitude)
Lons=list(DF.longitude)
X=list(DF["X"])
Y=list(DF["Y"])
geo=list(DF["geo_source"])
for i in range(len(scores)):
    s=scores[i]
    t=Addr_type[i]
    if s!="":
        if float(s)>=90 and t in types:
            Lats[i] = Y[i]
            Lons[i] = X[i]
            geo[i] = "AGOL"

DF['latitude'] = Lats
DF['longitude'] = Lons
DF['geo_source'] = geo

DF.to_csv("ODEFv2_Geocoded_AGOL_29-03-2021.csv", index=False)