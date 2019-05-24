import pandas as pd
import re


long_sub_en={'avenue':'av',
	'boulevard':'blvd',
	'by-pass':'bypass',

	'circle':'cir',
	'circuit':'circt',
	'concession':'conc',
	'court':'cour',
	'crescent':'cres',
	'corners':'crnrs',
	'crossing':'cross',
	'crossroad':'crossrd',
	'court':'crt',
	'diversion':'divers',
	'drive':'dr',	
	'esplanada':'espl',
	'estates':'estate',
	'expressway':'expy',
	'extension':'exten',
	'freeway':'fwy',
	'gardens':'gdns',
	'harbour':'harbr',
	'grounds':'grnds',
	'highlands':'hghlds',
	'heights':'hts',
	'highway':'hwy',
	'laneway':'lanewy',
	'lookout':'lkout',
	'limits':'lmts',
	'mountain':'mtn',
	'orchard':'orch',
	'passage':'pass',
	'park':'pk',
	'parkway':'pky',
	'place':'pl',
	'plateau':'plat',
	'promenade':'prom',
	'point':'pt',
	'pathway':'ptway',
	'plateau':'plat',
	'private':'pvt',
	'promenade':'prom',
	'road':'rd',
	'range':'rg',
	'route':'rte',
	'rightofway':'rtofwy',
	'section':'sectn',
	'sideroad':'siderd',
	'square':'sq',
	'street':'st',
	'subdivision':'subdiv',
	'terrace':'terr',
	'townline':'tline',
	'tournabout':'trnabt',
	'village':'villge'
	}
	
dirs_en={'east':'e',
	'west':'w',
	'north':'n',
	'south':'s',
	'northeast':'ne',
	'north-east':'ne',
	'northwest':'nw',
	'north-west':'nw',
	'southeast':'se',
	'south-east':'se',
	'southwest':'sw',
	'south-west':'sw'
	}

def AddressClean_en(df,name_in, name_out):
	dirs=dirs_en
	long_sub=long_sub_en
	#get rid of periods
	df[name_out]=[x.replace('.','') for x in df[name_in].astype('str')]
	#make all lower case
	df[name_out]=df[name_out].str.lower()


	#Loop through directions and  shorten as required:

	for i,j in dirs.items():
	
		#shorten directions only if they are the last word of the string
		expr=r"\b"+re.escape(i)+r"$"
		df[name_out]=df[name_out].replace(regex=expr,value=j)
		#shorten directions if they are first word in string:
		expr=r"^"+re.escape(i)+r"\b"
		df[name_out]=df[name_out].replace(regex=expr,value=j)

	#Loop through road types and shorten as required:
	##FOR ENGLISH

	for i,j in long_sub.items():

		#shorten street types if they are last word:
		expr=r"\b"+re.escape(i)+r"$"
		df[name_out]=df[name_out].replace(regex=expr,value=j)

		#shorten street types if the last word is 'e','n','s',or 'w', and the matched expression immediately precedes it
		for longdir,shortdir in dirs.items():
			expr=r"\b"+re.escape(i)+" "+re.escape(shortdir)+r"$"
			sub=j+" "+shortdir
			df[name_out]=df[name_out].replace(regex=expr,value=sub)
		
	return df
##FOR FRENCH	

def AddressClean_fr(df, name_in, name_out):

	long_sub={'autoroute':'aut',
	'avenue':'ave',
	'boulevard':'boul',
	'barrage':'brge',
	'centre':'c',
	'carré':'car',
	'cul-de-sac':'cds',
	'chemin':'ch',
	'carrefour':'carref',
	'croissant':'crois',
	'échangeur':'éch',
	'esplanada':'espl',
	'impasse':'imp',
	'passage':'pass',
	'plateau':'plat',
	'promenade':'prom',
	'rond-point':'rdpt',
	'ruelle':'rle',
	'route':'rte',
	'sentier':'sent',
	'terrasse':'tsse',
	}



	dirs={'est':'e',
	'ouest':'o',
	'nord':'n',
	'sud':'s',
	'nordest':'ne',
	'nord-est':'ne',
	'nordouest':'no',
	'nord-ouest':'no',
	'sudest':'se',
	'sud-est':'se',
	'sudouest':'so',
	'sud-ouest':'so'

	}

	#get rid of periods
	df[name_out]=[x.replace('.','') for x in df[name_in].astype('str')]

	for i,j in dirs.items():
	
		#shorten directions only if they are the last word of the string
		expr=r"\b"+re.escape(i)+r"$"
		df[name_out]=df[name_out].replace(regex=expr,value=j)
		 

	for i,j in long_sub.items():

		#shorten street types if they are first word in string:
		expr=r"^"+re.escape(i)+r"\b"
		df[name_out]=df[name_out].replace(regex=expr,value=j)

	return df

