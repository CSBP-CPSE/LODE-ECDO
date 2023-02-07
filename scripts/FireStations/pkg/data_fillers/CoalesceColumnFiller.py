'''
File:    CoalesceColumnFiller.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Fill columns from other columns

Created on: 2023-02-07
'''

from .StaticColumnFiller import StaticColumnFiller
import tempfile

class CoalesceColumnFiller(StaticColumnFiller):

    def __init__(self, cfg):
        super().__init__(cfg)
        self._coalesce = cfg["coalesce"]
        self._sfx =  next(tempfile._get_candidate_names())

    def fill_data(self):
        if self._data_filled:
            return True

        super().fill_data()

        self._data_filled = False
        
        if self._coalesce is not None:
            for newcol, cols in self._coalesce.items():

                self._logger.debug("%s filling column %s <- %s" % (self, newcol, cols))

                self._data[newcol] = self._data[cols].bfill(axis=1).iloc[:, 0]

        self._data_filled = True

        return True