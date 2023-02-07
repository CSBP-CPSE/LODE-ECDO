'''
File:    SameCSDDifferentSourceBlocker.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Helper class to block on same CSD but different sources

Created on: 2023-02-07
'''

from recordlinkage.base import BaseIndexAlgorithm
from pandas import MultiIndex

class SameCSDDifferentSourceBlocker(BaseIndexAlgorithm):
    """
    Helper class to block on same CSD but different sources
    """

    def __init__(self, block_field="CSDUID", source_field="source_id", verify_integrity=True, suffixes=...):
        super().__init__(verify_integrity, suffixes)
        self._block_field = block_field
        self._source_field = source_field

    def _link_index(self, df_a, df_b):
        # cross product, block by field
        df = df_a[[self._block_field, self._source_field]].reset_index() \
            .merge( df_b[[self._block_field, self._source_field]].reset_index(), 
                    on=self._block_field, 
                    how="inner", 
                    suffixes=("_A", "_B"))

        # keep only those with different source IDs
        df = df[df["%s_A" % self._source_field] != df["%s_B" % self._source_field]]

        return MultiIndex.from_frame(df[["index_A", "index_B"]], names=["level_0", "level_1"])