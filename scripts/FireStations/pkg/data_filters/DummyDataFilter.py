'''
File:    DummyDataFilter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for data Filters

Created on: 2023-01-30
'''

from .DataFilter import DataFilter

class DummyDataFilter(DataFilter):

    def __init__(self, cfg):
        super().__init__(cfg)
        self._data_filtered = True

    def filter_data(self):
        if self._data_filtered:
            return True
        
        self._data_filtered = True

        return True