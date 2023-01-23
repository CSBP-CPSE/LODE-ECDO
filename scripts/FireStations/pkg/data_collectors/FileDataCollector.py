'''
File:    FileDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Collector to read data extracted on file, e.g. by Scrapy

Created on: 2023-01-18
'''

import os

from .DataCollector import DataCollector

class FileDataCollector(DataCollector):
    """
    Collector to read data extracted on file, e.g. by Scrapy
    """

    def __init__(self, cfg):
        self._file = cfg['file']
        self._data_type = cfg["data_type"]
        self._data = None

        return

    def get_data(self):
        # Check if data has been read into memory
        if self.check_data_loaded():
            return True

        # if not, check if data file is availble
        if os.path.exists(self._file):
            self._logger.info("%s reading data from cache: %s" % (self, self._file))
            with open(self._file, "r", encoding="utf8") as f:
                self._data = f.read()
                self._logger.info("%s data read." % self)
                return True

        return False