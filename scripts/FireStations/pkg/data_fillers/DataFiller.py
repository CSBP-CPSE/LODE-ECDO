'''
File:    DataFiller.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for data Fillers

Created on: 2023-01-30
'''


from abc import ABC, abstractmethod
import abstract_classes.PipelineElement as PipelineElement

class DataFiller(PipelineElement, ABC):

    def __init__(self, cfg):
        self._cfg = cfg
        self._source = None
        self._sink = None
        self._data = None
        self._data_filled = False

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
            self.fill_data()
        return self._data

    @abstractmethod
    def fill_data(self):
        pass

    def set_logger(self, logger):
        self._logger = logger
