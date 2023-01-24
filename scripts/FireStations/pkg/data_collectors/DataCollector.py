'''
File:    DataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for data collectors

Created on: 2023-01-17
'''

import os

import abstract_classes.PipelineElement as PipelineElement
import abstract_classes.CachedElement   as CachedElement

class DataCollector(PipelineElement, CachedElement):
    """
    Base class for data collectors
    """

    def __init__(self, cfg):
        self._url = cfg['url']
        self._data_type = cfg["data_type"]
        self._data = None

    def set_source(self, src):
        # data collectors are prime sources
        pass

    def pass_data(self):
        if not self._data:
            self.get_data()
        return self._data

    def set_logger(self, logger):
        self._logger = logger  

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

    def cache_data(self):
        o_f = os.path.join(self._cache_dir, self._cache_file)
        self._logger.info("%s saving data to: %s" % (self, o_f))
        with open(os.path.join(self._cache_dir, self._cache_file), "w", encoding="utf8") as f:
            f.write(self._data)
            self._logger.info("%s data saved." % self)
            return True

    def retrieve_cached_data(self):
        if self.data_cache_exists():
            o_f = os.path.join(self._cache_dir, self._cache_file)
            self._logger.info("%s reading data from cache: %s" % (self, o_f))
            with open(o_f, "r", encoding="utf8") as f:
                self._data = f.read()
                self._logger.info("%s data read." % self)
                return True
        return False