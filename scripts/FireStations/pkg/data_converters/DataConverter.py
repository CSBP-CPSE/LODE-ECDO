'''
File:    DataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for data converters

Created on: 2023-01-23
'''

from abc import ABC, abstractmethod
import os
import geopandas as gpd
import abstract_classes.PipelineElement as PipelineElement
import abstract_classes.CachedElement as CachedElement

class DataConverter(PipelineElement, CachedElement, ABC):
    """
    Base class for data converters
    """

    def __init__(self, cfg):
        self._source = None
        self._data = None
        self._data_converted = False
        self._source = None
        self._sink = None

    @abstractmethod
    def convert_data(self):
        pass

    def set_source(self, src):
        self._source = src
        self._source.set_sink(self)

    def set_sink(self, snk):
        self._sink = snk

    def set_logger(self, logger):
        self._logger = logger

    def pass_data(self):
        if not self._data_converted:
            self.convert_data()
        if self._data_converted and not self.data_cache_exists():
            self.cache_data()
        return self._data

    def set_cache_dir(self, d):
        self._cache_dir = d

    def set_cache_file(self, f):
        self._cache_file = f

    def check_data_loaded(self):
        if self._data:
            self._logger.info("%s data in memory." % self)
            return True
        else:
            return False

    def data_cache_exists(self):
        return os.path.exists(os.path.join(self._cache_dir, self._cache_file))

    # TODO: use parquet for data caching
    def cache_data(self):
        o_f = os.path.join(self._cache_dir, self._cache_file)
        self._logger.info("%s saving data to: %s" % (self, o_f))
        self._data.to_file(o_f, driver="GeoJSON")
        self._logger.info("%s data saved." % self)
        return True

    def retrieve_cached_data(self):
        if self.data_cache_exists():
            o_f = os.path.join(self._cache_dir, self._cache_file)
            self._logger.info("%s reading data from cache: %s" % (self, o_f))
            self._data = gpd.GeoDataFrame.from_file(o_f)
            return True
        return False