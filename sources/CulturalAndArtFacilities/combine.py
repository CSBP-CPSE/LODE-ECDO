import pandas as pd
import glob

path = r'C:\Users\Ash\.opentabulate\pddir\clean' # use your path
all_files = glob.glob(path + "/*.csv")

version = "combinedArtsAndCulture_03172020_v4"
orderedCol = ['facility_name','facility_type','address_concat','unit','street_no','street_name','address_full','postcode','city','prov/terr','data_city','data_prov/terr','data_provider','file_type','latitude','longitude','ERROR']
li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, encoding='cp1252')
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_csv( version + ".csv", index=False, encoding='utf-8-sig')

filtersRemove = ["make up", "makeup", "cabinet", "artistry"]

frame_filter = pd.concat(li, axis=0, ignore_index=True)
for f in filtersRemove:
    frame_filter = frame[(~frame["library_name"].str.contains(f, na=False))&(~frame["library_type"].str.contains(f, na=False))]

oname = ["library_name", "library_type"]
nname = ["facility_name", "facility_type"]

for i in range(0, len(oname)):
    frame_filter.rename(columns={oname[i]: nname[i]},inplace=True)

frame_filter =  frame_filter[orderedCol]

frame_filter.to_csv( version + "_filtered.csv", index=False, encoding='utf-8-sig')