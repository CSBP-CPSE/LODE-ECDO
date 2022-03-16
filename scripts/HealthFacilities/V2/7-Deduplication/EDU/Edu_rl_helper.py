# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:34:22 2020

@author: josep

Helper functions for the recordlinkage script
"""

import pandas as pd
import re
import unicodedata
from numpy import cos, sin, arcsin, sqrt
from math import radians

def strip_accents(text):
    text=str(text)
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

#distance calculation

def haversine(row):
    lon1 = row['Longitude_1']
    lat1 = row['Latitude_1']
    lon2 = row['Longitude_2']
    lat2 = row['Latitude_2']
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * arcsin(sqrt(a)) 
    D = 6371 * c
    return D


#address standardization - includes province names to their abbreviations

en_sub={'alberta': 'ab',
        'manitoba': 'mb',
        'british columbia': 'bc',
        'new brunswick': 'nb',
        'newfoundland': 'nl',
        'newfoundland and labrador': 'nl',
        'nova scotia': 'ns',
        'ontario': 'on',
        'quebec': 'qc',
        'prince edward island': 'pe',
        'saskatchewan': 'sk',
        'northwest territories': 'nt',
        'nunavut': 'nu',
        'yukon territories': 'yt',
    'avenue': 'av',
    'ave': 'av',
	'boulevard':'blvd',
	'by-pass':'bypass',
	'circle':'cir',
	'circuit':'circt',
	'concession':'conc',
	'crescent':'cres',
	'corners':'crnrs',
	'crossing':'cross',
	'crossroad':'crossrd',
	'court':'crt',
	'diversion':'divers',
	'drive':'dr',	
	'esplanade':'espl',
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

en_dirs={'east':'e',
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

fr_sub={'autoroute':'aut',
	'avenue':'av',
    'ave':'av',
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

fr_dirs={'est':'e',
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

def AddressClean(text,lang='en'):
    #reads in string, makes replacements of street types and directions
    #specify the language you want to use, default is english
    if lang=='en':
        sub=en_sub
        dirs=en_dirs
    elif lang=='fr':
        sub=fr_sub
        dirs=fr_dirs
    else:
        print("specify lang='en' or lang='fr'")
        return
    #replace periods
    text=text.replace('.','')
    
    r"""
    Another version of AddressClean is 'smart', in the sense that it only
    shortens directions or street types in certain contexts (see version on github)
    because we're applying this to both street names and whole address strings,
    those rules aren't likely to work terribly well
    so we'll apply them universally, and hope for the best
    """
    
    		
    for i,j in dirs.items():
    	
    	expr=re.compile(r"\b"+re.escape(i)+r"\b")
    	text=re.sub(expr,j,text)
    for i, j in sub.items():
        expr=re.compile(r"\b"+re.escape(i)+r"\b")
        text=re.sub(expr,j,text)
        
    return text