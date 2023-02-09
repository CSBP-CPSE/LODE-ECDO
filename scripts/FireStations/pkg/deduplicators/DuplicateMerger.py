'''
File:    DuplicateMerger.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Determine duplicates from features and merge data

Created on: 2023-02-07
'''

from pandas import concat, MultiIndex
from recordlinkage import ECMClassifier

from .Deduplicator import Deduplicator

class DuplicateMerger(Deduplicator):

    def __init__(self, cfg) -> None:
        super().__init__(cfg)
        self._fields = cfg["dedupe_fields"]
        self._metrics = cfg["dedupe_metrics"]
        self._threshold = cfg["threshold"]

    def process_data(self):
        self._data = self.predict_merge_features(self._data)

        self._data_processed = True

        return True

    def predict_merge_features(self, df):

        # feature columns
        feature_cols = [i for i in df.columns if i[-2:] in ["_A", "_B"] or (i in self._metrics)]
        
        # keep away data not to be processed
        no_features = self.__data_no_process(df, feature_cols)
        
        features    = df.loc[ df["__DEDUPE_PROCESSING__"], feature_cols].copy()
        features.index = MultiIndex.from_tuples(features.index)

        # predict links from features
        test = features[self._metrics]

        ec = ECMClassifier(binarize=self._threshold)
        predict_links = ec.fit_predict(test)
        
        print("Predicted links: %d" % len(predict_links))
                
        # retain unmatched features, to skip merging
        unmatch_A = self.__unmatched_features(features, predict_links, 0, df.crs)
        unmatch_B = self.__unmatched_features(features, predict_links, 1, df.crs)
        
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
                .fillna("")\
                .apply(self.__copy_longest_string, raw=True, axis=1)
            
        merged_features.index = merged_features.index.get_level_values(0).rename("index")
        
        merged_features = merged_features.set_geometry("geometry")
        merged_features.set_crs(df.crs)
        
        merged_features["origin"] = "M"
                
        out_data = concat([no_features, unmatch_A, unmatch_B, merged_features], axis=0)

        out_data.drop_duplicates(inplace=True)

        # drop merged columns
        drop_cols = [i for i in out_data.columns if i.endswith("_A") or i.endswith("_B")]
        # also drop metrics
        drop_cols.extend(self._metrics)
        
        out_data.drop(columns=drop_cols, inplace=True)

        return out_data

    @staticmethod
    def __copy_longest_string(x):
        a = x[0]
        b = x[1]
        try:
            if (a is None) or (type(a) != str) or (len(a) > len(b)):
                return a
            else:
                return b
        except:
            print("typeA: %s valueA: %s typeB: %s valueB: %s" % (type(a), a, type(b), b))
            return a
        
    @staticmethod
    def __unmatched_features(df, predict_links, side, crs):
        if side == 0:
            letter = "A"
        elif side == 1:
            letter = "B"
        else:
            raise ValueError("Unknown feature side %s" % side)
            
        loc_A = ~(df.index.get_level_values(side).isin(predict_links.get_level_values(side)))
        col_A = [i for i in df.columns if i.endswith("_%s" % letter)]
        unmatch_A = df.loc[loc_A, col_A].rename(columns=dict([(i,i[:-2]) for i in col_A])).drop(columns="index")
        unmatch_A["origin"] = letter
        unmatch_A.index = unmatch_A.index.get_level_values(side).rename("index")
        unmatch_A.drop_duplicates(inplace=True)
        unmatch_A = unmatch_A.set_geometry("geometry")
        unmatch_A.set_crs(crs)
 
        return unmatch_A

    @staticmethod
    def __data_no_process(df, feature_cols):
        no_features = df.loc[~df["__DEDUPE_PROCESSING__"], [i for i in df.columns if i not in feature_cols]].copy()
        no_features["origin"] = "U"
        no_features.drop("__DEDUPE_PROCESSING__", axis=1, inplace=True)
        no_features = no_features.set_geometry("geometry")
        no_features.set_crs(df.crs)
        return no_features