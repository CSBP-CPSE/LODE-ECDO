import pandas as pd
from Address_Format_Funcs import AddressClean_en, AddressClean_fr


test=pd.read_csv('example.csv')

test=AddressClean_en(test,'street_name','formatted_en')
test=AddressClean_fr(test,'street_name','formatted_fr')

test.to_csv('example_formatted.csv',index=False)
