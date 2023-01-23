'''
File:    AbstractDataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for data converters

Created on: 2023-01-23
'''

from abc import ABC, abstractmethod

class AbstractDataConverter(ABC):
    """
    Abstract class for data converters
    """

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def convert_data(self):
        pass

    def set_data_source(self, src):
        self._source = src

    def set_logger(self, logger):
        self._logger = logger

    def pass_data(self):
        if not self._data_converted:
            self.convert_data()
        return self._data