'''
File:    DummyDataTabulator.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Dummy Data Tabulator

Created on: 2023-01-30
'''

from .DataTabulator import DataTabulator

class DummyDataTabulator(DataTabulator):

    def __init__(self, cfg):
        super().__init__(cfg)
        self._data_tabulated = True


    def tabulate(self):
        if self._data_tabulated:
            return True
        else:
            self._data_tabulated = True
            return True