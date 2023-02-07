'''
File:    StaticColumnFiller.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Fill columns with metadata

Created on: 2023-01-30
'''

from .DataFiller import DataFiller

class StaticColumnFiller(DataFiller):

    def __init__(self, cfg):
        super().__init__(cfg)
        self._fill_ins = cfg["fill_ins"]

    def fill_data(self):
        if self._data_filled:
            return True
        
        self._logger.debug("%s filling columns %s" % (self, self._fill_ins))

        # fill columns with data from source definition
        # TODO: avoid data already filled?
        for column in self._fill_ins:
            self._data[column] = self._cfg[column]

        self._data_filled = True

        return True