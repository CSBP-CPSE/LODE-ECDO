'''
File:    DuplicateMerger.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Determine duplicates from features and merge data

Created on: 2023-02-07
'''

from pandas import concat
from recordlinkage import ECMClassifier

class DuplicateMerger(object):

    def __init__(self, fields, metrics) -> None:
        self._fields = fields
        self._metrics = metrics

    def predict_merge_features(self, features, threshold):

        test = features[self._metrics]

        ec = ECMClassifier(binarize=threshold)
        predict_links = ec.fit_predict(test)
        
        print("Predicted links: %d" % len(predict_links))
                
        # retain unmatched features, to skip merging
        loc_A = ~(features.index.get_level_values(0).isin(predict_links.get_level_values(0)))
        col_A = [i for i in features.columns if i.endswith("_A")]
        unmatch_A = features.loc[loc_A, col_A].rename(columns=dict([(i,i[:-2]) for i in col_A])).drop(columns="index")
        #unmatch_A["origin"] = "A"
        unmatch_A.index = unmatch_A.index.get_level_values(0).rename("index")
        unmatch_A.drop_duplicates(inplace=True)
        unmatch_A.set_geometry("geometry")

        loc_B = ~(features.index.get_level_values(1).isin(predict_links.get_level_values(1)))
        col_B = [i for i in features.columns if i.endswith("_B")]
        unmatch_B = features.loc[loc_B, col_B].rename(columns=dict([(i,i[:-2]) for i in col_B])).drop(columns="index")
        #unmatch_B["origin"] = "B"
        unmatch_B.index = unmatch_B.index.get_level_values(1).rename("index")
        unmatch_B.drop_duplicates(inplace=True)
        unmatch_B.set_geometry("geometry")
        
        merged_features = features.loc[predict_links, ].copy()
        merged_features.drop(columns=["index_A", "index_B"], inplace=True) 
        
        # use a simple backfill to merge A and B columns
        # that are not involved in the matching process
        colz = [i[:-2] for i in merged_features.columns if (i not in self._fields) and (i not in self._metrics) and (i[:-2] != "geometry")]
        
        for i in colz:            
            merged_features[i] = merged_features.loc[:, ["%s_A" % i, "%s_B" % i]]\
                .bfill(axis=1).iloc[:, 0]

        # keep geometry A
        merged_features["geometry"] = merged_features["geometry_A"]
            
        # keep "longest" features, hopefully it contains more information
        for i in self._fields:
            merged_features[i] = merged_features[["%s_A" % i, "%s_B" % i]]\
                .apply(self.__copy_longest_string, raw=True, axis=1)
            
        # drop merged columns
        drop_cols = [i for i in merged_features.columns if i.endswith("_A") or i.endswith("_B")]
        # also drop metrics
        drop_cols.extend(self._metrics)
        
        merged_features.drop(columns=drop_cols, inplace=True)

        merged_features.index = merged_features.index.get_level_values(0).rename("index")
        
        merged_features.set_geometry("geometry")
        
        #merged_features["origin"] = "M"
        
        return concat([unmatch_A, unmatch_B, merged_features], axis=0)

    @staticmethod
    def __copy_longest_string(x):
        a = x[0]
        b = x[1]
        if (a is None) or (type(a) != str) or (len(a) > len(b)):
            return a
        else:
            return b