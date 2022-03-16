# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:42:06 2020

@author: Joseph Kuchar (joseph.kuchar@canada.ca)
"""

import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn import preprocessing
import numpy as np

#read training data

df_train=pd.read_csv(r"C:\Users\josep\OneDrive\Work\ODHF\Deduplication\inputs\ODHF_CandidatePairs_Training_Update.csv"
                    ,encoding='cp1252')


le=preprocessing.LabelEncoder()
Y_train=le.fit_transform(df_train.Match)
X_train=df_train.drop(columns=['idx1','idx2','Name_1','Name_2','Address_1','Address_2',
                             'City_1','City_2','Match'])
X_train['Distance']=X_train['Distance']/X_train['Distance'].max()

#fit model to training data
clf = SGDClassifier(loss="hinge", penalty="l2",alpha=0.05)

clf.fit(X_train,Y_train)

#read in main data set to fit
DF=pd.read_csv(r"C:\Users\josep\OneDrive\Work\ODHF\Deduplication\outputs\ODHF_process_5a_candidate_pairs_FullInfo.csv",encoding='cp1252')
X=DF.drop(columns=['idx1','idx2','Name_1','Name_2','Address_1','Address_2',
                             'City_1','City_2'])
#I'm normalizing distance using the highest distance in the training set, as opposed
#to the full data - not sure what the best approach is
X['Distance']=X['Distance']/X_train['Distance'].max()
Y=clf.predict(X)


DF['Match']=Y
DF=DF.loc[DF.Match==1]

DF.to_csv(r"C:\Users\josep\OneDrive\Work\ODHF\Deduplication\outputs\ODHF_process_5b_candidate_pairs_FullInfo_Matched.csv",index=False,encoding='cp1252')