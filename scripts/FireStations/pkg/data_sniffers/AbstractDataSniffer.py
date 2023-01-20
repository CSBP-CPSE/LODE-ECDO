'''
File:    AbstractDataSniffer.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for data sniffers

Created on: 2023-01-20
'''

from abc import ABC, abstractmethod

class AbstractDataSniffer(ABC):

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def set_data_source(self, src):
        pass

    @abstractmethod
    def get_attributes(self):
        """
        Get list of data attributes
        """
        pass

    def pass_data(self):
        return self._data

    def set_logger(self, logger):
        self._logger = logger
