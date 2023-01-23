'''
File:    DataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for data converters

Created on: 2023-01-23
'''

from abc import ABC, abstractmethod
import abstract_classes.PipelineElement as PipelineElement

class DataConverter(PipelineElement, ABC):
    """
    Base class for data converters
    """

    def __init__(self, cfg):
        self._source = None
        self._data = None
        self._data_converted = False

    @abstractmethod
    def convert_data(self):
        pass

    def set_source(self, src):
        self._source = src

    def set_logger(self, logger):
        self._logger = logger

    def pass_data(self):
        if not self._data_converted:
            self.convert_data()
        return self._data