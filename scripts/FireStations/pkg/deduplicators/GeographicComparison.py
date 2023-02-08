'''
File:    GeographicComparison.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for geography-based deduplication

Created on: 2023-02-03
'''

from recordlinkage.standardise import clean
import recordlinkage as rl
import pandas as pd
import tempfile

from .Deduplicator import Deduplicator
from .SameCSDDifferentSourceBlocker import SameCSDDifferentSourceBlocker

class GeographicComparison(Deduplicator):
    """
    Class for geography-based deduplication
    """

    def __init__(self, cfg):
        super().__init__(cfg)

        self._fields = cfg["dedupe_fields"]

        self._indexer = rl.Index()
        self._indexer.add(SameCSDDifferentSourceBlocker())

        self._distance_offset_km = cfg["distance_offset_m"] / 1e3
        self._distance_scale_km  = cfg["distance_scale_m"]  / 1e3

        self._sfx = "_%s" % next(tempfile._get_candidate_names())

    def process_data(self):
        if self._data_processed:
            return True

        if self._data is None:
            self.get_data()

        self.__clean_strings()

        dA = self._data.copy()

        # add geometries
        dA["x%s" % self._sfx] = dA.geometry.x
        dA["y%s" % self._sfx] = dA.geometry.y

        candidate_links = self._indexer.index(dA)

        self._logger.debug("%s running fuzzy match on %d candidates." % (self, len(candidate_links)))

        fuzzy_matches = self.__link_fuzzy(candidate_links, dA)

        all_matches  = fuzzy_matches #pd.concat([exact_matches, fuzzy_matches], axis=0) 

        merged_matches = self.__merge_matches(dA, dA, all_matches)
        merged_matches["__DEDUPE_PROCESSING__"] = True

        # keep data not matched
        unmatched = self._data[ (~self._data.index.isin(merged_matches.index.get_level_values(0))) & 
                                (~self._data.index.isin(merged_matches.index.get_level_values(1))) ].copy()
        unmatched["__DEDUPE_PROCESSING__"] = False
        unmatched.set_crs(dA.crs)

        self._logger.debug("%s original data not in matched features: %d" % 
            (self, len(unmatched)))

        self._data = pd.concat([merged_matches, unmatched])
        
        # drop auxiliary columns
        self._data = self._data.drop(columns=[i for i in self._data.columns if self._sfx in i])

        # drop auxiliary columns

        self._data_processed = True

        return True

    @staticmethod
    def __merge_matches(dA, dB, matches):

        # use some axis tricks to get named multilevel index
        idx_lvl = ["level_0","level_1"]
        matches = matches.reset_index()
        m_index = matches[idx_lvl]
        matches = matches.set_index(idx_lvl)

        # keep data from first subset using left index
        mA = dA.reset_index()\
            .merge(m_index, left_on="index", right_on="level_0")\
            .set_index(idx_lvl) 

        # keep data from second subset using right index
        mB = dB.reset_index()\
            .merge(m_index, left_on="index", right_on="level_1")\
            .set_index(idx_lvl) 

        # join the two subsets, and the features
        out_data = mA.join(mB, lsuffix="_A", rsuffix="_B").join(matches)
        out_data = out_data.set_geometry("geometry_A") # just to keep geopandas quiet
        out_data.set_crs(dA.crs)
        return out_data

    def __clean_strings(self):
        self._logger.info("%s preprocessing data." % self)
        for i in self._fields:
            self._data["%s%s" % (i, self._sfx)] = clean(self._data[i], strip_accents="unicode")

    def __link_exact(self, links, dA, dB=None):
        self._logger.info("%s linking data (exact matches)." % self)

        compare = rl.Compare()

        for i in self._fields:
            i_str = "%s%s" % (i, self._sfx)
            compare.exact(i_str, i_str,  label='%s_ex' % i)

        features = compare.compute(links, dA, dB)

        return features

    def __link_fuzzy(self, links, dA, dB=None):
        self._logger.info("%s linking data (fuzzy matches)." % self)

        compare = rl.Compare()

        for i in self._fields:
            i_str = "%s%s" % (i, self._sfx)
            compare.string(i_str, i_str, method='cosine',  label='%s_cs' % i)

        x_str = "x%s" % self._sfx
        y_str = "y%s" % self._sfx

        compare.geo(x_str, y_str, x_str, y_str, 
            method="gauss", 
            label="gd_gauss", 
            offset=self._distance_offset_km , 
            scale=self._distance_scale_km)

        features = compare.compute(links, dA, dB)

        return features

