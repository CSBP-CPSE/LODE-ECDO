'''
File:    Deduplicator.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for Deduplicators

Created on: 2023-02-03
'''

from abc import ABC, abstractmethod
import abstract_classes.PipelineElement as PipelineElement

class Deduplicator(PipelineElement, ABC):
    """
    Abstract class for Deduplicators
    """

    def __init__(self, cfg):
        self._source = None
        self._data = None
        self._data_processed = False

    @abstractmethod
    def process_data(self):
        pass

    def set_source(self, src):
        self._source = src

    def set_logger(self, logger):
        self._logger = logger

    def get_data(self):
        self._data = self._source.pass_data()

    def pass_data(self):
        if self._data is None:
            self.get_data()
        if not self._data_processed:
            self.process_data()
        return self._data
