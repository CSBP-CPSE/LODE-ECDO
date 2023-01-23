'''
File:    CachedElement.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for element data caching

Created on: 2023-01-23
'''

from abc import ABC, abstractmethod

class CachedElement(ABC):
    """
    Abstract class for element data caching
    """

    @abstractmethod
    def set_cache_dir(self, d):
        pass

    @abstractmethod
    def set_cache_file(self, f):
        pass

    @abstractmethod
    def cache_data(self):
        pass

    @abstractmethod
    def retrieve_cached_data(self):
        pass

    @abstractmethod
    def data_cache_exists(self):
        pass