'''
File:    Geocoder.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for Geocoders

Created on: 2023-01-31
'''

from abc import ABC, abstractmethod
import abstract_classes.PipelineElement as PipelineElement

class Geocoder(PipelineElement, ABC):
    """
    Abstract class for Geocoders
    """

    def __init__(self, cfg):
        self._source = None
        self._sink = None
        self._data = None
        self._data_geocoded = False

    @abstractmethod
    def geocode_data(self):
        pass

    def set_source(self, src):
        self._source = src
        self._source.set_sink(self)

    def set_sink(self, snk):
        self._sink = snk

    def set_logger(self, logger):
        self._logger = logger

    def get_data(self):
        self._data = self._source.pass_data()

    def pass_data(self):
        if self._data is None:
            self.get_data()
        if not self._data_geocoded:
            self.geocode_data()
        return self._data
