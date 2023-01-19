'''
File:    AbstractDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for data collectors

Created on: 2023-01-17
'''

from abc import ABC, abstractmethod

class AbstractDataCollector(ABC):
    """
    Abstract class for data collectors
    """

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_reference(self):
        pass

    @abstractmethod
    def set_output_dir(self):
        pass

    @abstractmethod
    def set_output_file(self):
        pass    

    @abstractmethod
    def save_data(self):
        pass

    @abstractmethod
    def set_logger(self, logger):
        pass