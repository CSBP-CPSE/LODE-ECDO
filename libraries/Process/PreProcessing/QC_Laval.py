#This pre-processes Laval libraries.
#The original source includes many public buildings, so we restrict to libraries

import pandas as pd
import re

df=pd.read_csv('/home/csis/codes/OpenTabulate/Libraries/lieux_Laval.csv')

df=df.loc[df["type-commun"]=="Bibliothèque"]

f_out='/home/csis/codes/OpenTabulate/pddir/raw/QC_Laval_Libraries.csv'
df.to_csv(f_out)
