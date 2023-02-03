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

class GeographicDeduplicator(Deduplicator):
    """
    Class for geography-based deduplication
    """

    def __init__(self, cfg):
        super().__init__(cfg)
        # TODO: configurable deduplication parameters
        self._fields = cfg["dedupe_fields"]

        self._indexer = rl.Index()
        self._indexer.block(cfg["dedupe_block"])

        self._distance_offset_km = cfg["distance_offset_m"] / 1e3
        self._distance_scale_km  = cfg["distance_scale_m"]  / 1e3

        self._deduped_data_frame = None
        sfx =  next(tempfile._get_candidate_names())
        # create random suffixes to store temporary data used for matching
        self._suffixes = {  "match": "_match_%s" % sfx, 
                            "string": "_string_%s" % sfx}

    def dedupe_data(self):
        if self._data_deduped:
            return True

        if self._data is None:
            self.get_data()

        self.__clean_strings()

        # split data into multiple parts
        # TODO: make it configurable
        dA = self._data[self._data.source_id == 22].copy()
        dB = self._data[self._data.source_id != 22].copy()

        # add geometries
        sfx = self._suffixes["string"]
        dA["x%s" % sfx] = dA.geometry.x
        dA["y%s" % sfx] = dA.geometry.y
        dB["x%s" % sfx] = dB.geometry.x
        dB["y%s" % sfx] = dB.geometry.y

        candidate_links = self._indexer.index(dA, dB)

        self._logger.debug("%s running exact match on %d candidates." % (self, len(candidate_links)))

        exact_matches = self.__link_exact(candidate_links, dA, dB)

        self._logger.debug("%s found %d exact matches." % (self, len(exact_matches)))

        # drop exact matches from links
        candidate_links = candidate_links[~(candidate_links.get_level_values(0).isin(exact_matches.index.get_level_values(0)) |\
                                            candidate_links.get_level_values(1).isin(exact_matches.index.get_level_values(1)))] 
        self._logger.debug("%s running fuzzy match on %d candidates." % (self, len(candidate_links)))

        fuzzy_matches = self.__link_fuzzy(candidate_links, dA, dB)

        all_matches  = pd.concat([exact_matches, fuzzy_matches], axis=0) 

        #self._data = self.__merge_matches(dA, dB, all_matches)

        overwrite_data = self.__merge_overwrite_data(dA, dB, all_matches)

        # drop auxiliary columns
        for sfx in self._suffixes.values():
            overwrite_data = overwrite_data.drop(columns=[i for i in overwrite_data.columns if i.endswith(sfx)])

        self._data = overwrite_data

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
        sfx = self._suffixes["match"]

        change_data = change_data.join(mB, rsuffix=sfx)

        # Overwrite data if missing
        for i in self._fields:
            change_data.loc[change_data[i].isna(), i] = change_data.loc[change_data[i].isna(), "%s%s" % (i, sfx)]

        change_data.drop(columns=["index"] + [i for i in change_data.columns if i.endswith(sfx)], inplace=True)

        # join the two subsets, and the features
        return pd.concat([keep_data, change_data], axis=0, ignore_index=True)

    def __clean_strings(self):
        # create random suffixes to store temporary data used for matching
        sfx = self._suffixes["string"]

        self._logger.info("%s preprocessing data." % self)
        for i in self._fields:
            self._data["%s%s" % (i, sfx)] = clean(self._data[i], strip_accents="unicode")

    def __link_exact(self, links, dA, dB=None):
        self._logger.info("%s linking data (exact matches)." % self)

        compare = rl.Compare()

        sfx = self._suffixes["string"]

        for i in self._fields:
            i_str = "%s%s" % (i, sfx)
            compare.exact(i_str, i_str,  label='%s_ex' % i)

        features = compare.compute(links, dA, dB)

        return features[features.sum(axis=1) >= 1]

    def __link_fuzzy(self, links, dA, dB=None):
        self._logger.info("%s linking data (fuzzy matches)." % self)

        compare = rl.Compare()

        sfx = self._suffixes["string"]

        for i in self._fields:
            i_str = "%s%s" % (i, sfx)
            compare.string(i_str, i_str, method='cosine',  label='%s_cs' % i)

        x_str = "x%s" % sfx
        y_str = "y%s" % sfx

        compare.geo(x_str, y_str, x_str, y_str, 
            method="gauss", 
            label="gd_gauss", 
            offset=self._distance_offset_km , 
            scale=self._distance_scale_km)

        features = compare.compute(links, dA, dB)

        return features[features.sum(axis=1) >= 1]

