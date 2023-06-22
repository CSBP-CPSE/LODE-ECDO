'''
File:    PipelineElement.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for pipeline elements

Created on: 2023-01-23
'''

from abc import ABC, abstractmethod

class PipelineElement(ABC):
    """
    Abstract class for data collectors
    """

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def set_logger(self, logger):
        pass

    @abstractmethod
    def set_source(self, src):
        pass

    @abstractmethod
    def set_sink(self, snk):
        pass

    def get_source(self):
        return self._source

    def get_sink(self):
        return self._sink

    @abstractmethod
    def pass_data(self):
        pass