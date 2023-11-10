import re
import pandas as pd

directions=['e','w','n','s','ne','nw','se','sw','no','so','o']

#check if the streets end in directions, and if so, make sure they are the same
def DirectionCheck(X):
	DIR_MATCH=True
	for dirn in directions:

		expr=' '+dirn
		check=X.str.endswith(expr)

		if check[0] != check[1]:
			#directions don't match, break 
			DIR_MATCH=False
			break
	return DIR_MATCH

#Check to see if the street name is a number (e.g., 93 av), and if so make sure they match
def NameIsNumber(X):
	NUM_MATCH=True
	x=re.search("^\d+[A-z]*",X[0]) #^: starts with, \d+: multicharacter number, [A-z]*: 0 or more letters 
	y=re.search("^\d+[A-z]*",X[1])
	
	#possible cases: Only one of these is a number (no match), they are both the same number (match) or they are both not numbers (possible match, return True)
	
	if ((x==None) and (y!=None)) or ((x!=None) and (y==None)):
		NUM_MATCH=False
	elif (x==None) and (y==None):
		NUM_MATCH=True 
	#if neither x or y are 'None', then they are number addresses, so we can check for a match
	elif (x.group()==y.group()): 
		NUM_MATCH=True
	else:
		NUM_MATCH=False
	
	return NUM_MATCH
	

