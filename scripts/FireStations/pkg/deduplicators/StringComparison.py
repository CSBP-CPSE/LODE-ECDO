'''
File:    StringComparison.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for string-based deduplication

Created on: 2023-02-03
'''

from recordlinkage.standardise import clean
import recordlinkage as rl
import pandas as pd
import tempfile
from .Deduplicator import Deduplicator

class StringComparison(Deduplicator):
    """
    Class for string-based deduplication
    """

    def __init__(self, cfg):
        super().__init__(cfg)
        # TODO: configurable deduplication parameters
        self._fields = cfg["dedupe_fields"]

        self._indexer = rl.Index()
        self._indexer.block(cfg["dedupe_block"])

        self._deduped_data_frame = None
        self._sfx =  next(tempfile._get_candidate_names())

    def process_data(self):
        if self._data_processed:
            return True

        if self._data is None:
            self.get_data()

        self.__clean_strings()


        candidate_links = self._indexer.index(self._data)

        self._logger.debug("%s running exact match on %d candidates." % (self, len(candidate_links)))

        exact_matches = self.__link_exact(candidate_links, self._data)

        self._logger.debug("%s found %d exact matches." % (self, len(exact_matches)))

        # drop exact matches from links
        candidate_links = candidate_links[~(candidate_links.get_level_values(0).isin(exact_matches.index.get_level_values(0)) |\
                                            candidate_links.get_level_values(1).isin(exact_matches.index.get_level_values(1)))] 
        self._logger.debug("%s running fuzzy match on %d candidates." % (self, len(candidate_links)))

        fuzzy_matches = self.__link_fuzzy(candidate_links, self._data)

        all_matches  = pd.concat([exact_matches, fuzzy_matches], axis=0) 

        self._data = self.__merge_matches(self._data, self._data, all_matches)  

        self._data = self._data.drop(columns=[i for i in self._data.columns if self._sfx in i])

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
        return mA.join(mB, lsuffix="_A", rsuffix="_B").join(matches)

    def __clean_strings(self):
        # create random suffixes to store temporary data used for matching

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
            compare.string(i_str, i_str, method='jarowinkler',  label='%s_jw' % i)

        features = compare.compute(links, dA, dB)

        return features

