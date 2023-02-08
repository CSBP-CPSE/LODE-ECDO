'''
File:    DataFilter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for data Filters

Created on: 2023-01-30
'''

import pandas as pd
import abstract_classes.PipelineElement as PipelineElement

class DataFilter(PipelineElement):

    def __init__(self, cfg):
        self._cfg = cfg
        self._source = None
        self._sink = None
        self._data = None
        self._filter_or  = cfg.get("filter_or", dict())
        self._filter_and = cfg.get("filter_and", dict())
        self._filter_not = cfg.get("filter_not", dict())
        self._data_filtered = False

    def set_source(self, src):
        self._source = src
        self._source.set_sink(self)

    def set_sink(self, snk):
        self._sink = snk

    def get_data(self):
        self._data = self._source.pass_data()

    def pass_data(self):
        if self._data is None:
            self.get_data()
        if self._data is not None:
            self.filter_data()
        return self._data

    def filter_data(self):
        if self._data_filtered:
            return True
        
        self._logger.debug("%s filtering rows %s" % (self, self._filter_or))

        # filter or
        if self._filter_or:
            locat_or = pd.concat([self._data[k].isin(v) for k,v in self._filter_or.items()], axis=1).apply(any, axis=1)
            self._data = self._data[locat_or].copy()

        # filter and
        if self._filter_and:
            locat_and = pd.concat([self._data[k].isin(v) for k,v in self._filter_and.items()], axis=1).apply(all, axis=1)
            self._data = self._data[locat_and].copy()

        # filter not
        if self._filter_not:
            locat_not = pd.concat([~self._data[k].isin(v) for k,v in self._filter_not.items()], axis=1).apply(all, axis=1)
            self._data = self._data[locat_not].copy()

        self._data_filtered = True

        return True

    def set_logger(self, logger):
        self._logger = logger
