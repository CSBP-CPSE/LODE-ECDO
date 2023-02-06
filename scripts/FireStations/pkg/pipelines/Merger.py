'''
File:    Merger.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Merger of pipeline data

Created on: 2023-02-06
'''

import pandas as pd
from abstract_classes.PipelineElement import PipelineElement

class Merger(PipelineElement):

    def __init__(self, cfg) -> None:
        self._data = None
        self._data_merged = False
        self._source = None
        self._logger = None

    def set_source(self, src):
        # Source can be a single element, or multiple
        # TODO: verify
        self._source = src
        
    def get_data(self):
        if self._data is None:
            self._data = self._source.pass_data()

        return True

    def set_logger(self, logger):
        self._logger = logger

    def pass_data(self):
        if self._data_merged:
            return self._data

        if self._data is None:
            self.get_data()

        # merge data 
        self._data = pd.concat(self._data, axis=0, ignore_index=True)

        self._data_merged = True

        self._logger.info("%s null geometries: %s" % (self, self._data.geometry.isnull().values.any()))
        self._logger.info("%s records: %d" % (self, len(self._data)))

        return self._data