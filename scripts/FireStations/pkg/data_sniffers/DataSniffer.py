'''
File:    DataSniffer.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for data sniffers

Created on: 2023-01-20
'''

from abc import ABC, abstractmethod
import abstract_classes.PipelineElement as PipelineElement

class DataSniffer(PipelineElement, ABC):

    def __init__(self, cfg):
        self._source = None
        self._data = None

    @abstractmethod
    def get_attributes(self):
        """
        Get list of data attributes
        """
        pass

    def set_source(self, src):
        self._source = src

    def pass_data(self):
        return self._data

    def set_logger(self, logger):
        self._logger = logger
