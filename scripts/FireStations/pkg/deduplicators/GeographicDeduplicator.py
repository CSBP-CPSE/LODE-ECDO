'''
File:    GeographicDeduplicator.py
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

class GeographicDeduplicator(Deduplicator):
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

        self._deduped_data_frame = None
        self._sfx = "_%s" % next(tempfile._get_candidate_names())

    def dedupe_data(self):
        if self._data_deduped:
            return True

        if self._data is None:
            self.get_data()

        self.__clean_strings()

        dA = self._data.copy()

        # add geometries
        dA["x%s" % self._sfx] = dA.geometry.x
        dA["y%s" % self._sfx] = dA.geometry.y

        candidate_links = self._indexer.index(dA)

        #self._logger.debug("%s running exact match on %d candidates." % (self, len(candidate_links)))

        #exact_matches = self.__link_exact(candidate_links, dA)

        #self._logger.debug("%s found %d exact matches." % (self, len(exact_matches)))

        # drop exact matches from links
        #candidate_links = candidate_links[~(candidate_links.get_level_values(0).isin(exact_matches.index.get_level_values(0)) |\
        #                                    candidate_links.get_level_values(1).isin(exact_matches.index.get_level_values(1)))] 

        self._logger.debug("%s running fuzzy match on %d candidates." % (self, len(candidate_links)))

        fuzzy_matches = self.__link_fuzzy(candidate_links, dA)

        all_matches  = fuzzy_matches #pd.concat([exact_matches, fuzzy_matches], axis=0) 

        self._data = self.__merge_matches(dA, dA, all_matches)

        #overwrite_data = self.__merge_overwrite_data(dA, dB, all_matches)

        # drop auxiliary columns
        self._data = self._data.drop(columns=[i for i in self._data.columns if self._sfx in i])

        self._data_deduped = True

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
        return mA.join(mB, lsuffix="_A", rsuffix="_B").join(matches)

    def __merge_overwrite_data(self, dA, dB, matches):

        # use some axis tricks to get named multilevel index
        idx_lvl = ["level_0","level_1"]
        matches = matches.reset_index()
        m_index = matches[idx_lvl]
        matches = matches.set_index(idx_lvl)

        # only data in left index needs to be changed
        keep_data = pd.concat([dA[~dA.index.isin(m_index["level_0"])], 
                               dB[~dB.index.isin(m_index["level_1"])]], axis=0)

        # keep data from first subset using left index
        change_data = dA.reset_index()\
            .merge(m_index, left_on="index", right_on="level_0")\
            .set_index(idx_lvl) 

        # keep data from second subset using right index
        mB = dB.reset_index()\
            .merge(m_index, left_on="index", right_on="level_1")\
            .set_index(idx_lvl) 

        # create suffix 
        change_data = change_data.join(mB, rsuffix=self._sfx)

        # Overwrite data if missing
        for i in self._fields:
            change_data.loc[change_data[i].isna(), i] = change_data.loc[change_data[i].isna(), "%s%s" % (i, self._sfx)]

        change_data.drop(columns=["index"])

        # join the two subsets, and the features
        return pd.concat([keep_data, change_data], axis=0, ignore_index=True)

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

        return features[features.sum(axis=1) > 0]

    def __link_fuzzy(self, links, dA, dB=None):
        self._logger.info("%s linking data (fuzzy matches)." % self)

        compare = rl.Compare()

        for i in self._fields:
            i_str = "%s%s" % (i, self._sfx)
            compare.exact(i_str, i_str, label='%s_ex' % i)
            compare.string(i_str, i_str, method='cosine',  label='%s_cs' % i)

        x_str = "x%s" % self._sfx
        y_str = "y%s" % self._sfx

        compare.geo(x_str, y_str, x_str, y_str, 
            method="gauss", 
            label="gd_gauss", 
            offset=self._distance_offset_km , 
            scale=self._distance_scale_km)

        features = compare.compute(links, dA, dB)

        return features[features.sum(axis=1) > 0]

