'''
File:    FileDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Collector to read data extracted on file, e.g. by Scrapy

Created on: 2023-01-18
'''

import os

from .AbstractDataCollector import AbstractDataCollector

class FileDataCollector(AbstractDataCollector):
    """
    Collector to read data extracted on file, e.g. by Scrapy
    """

    def __init__(self, cfg):
        self._file = cfg['file']
        self._reference = cfg["reference"]
        self._data_type = cfg["data_type"]
        self._data = None

        return

    def set_output_dir(self, d):
        self._output_dir = d

    def set_output_file(self, f):
        self._output_file = f

    def get_data(self):
        # Check if data has been read into memory
        if self._data:
            self._logger.info("%s data in memory." % self)
            return True

        # if not, check if data cache is availble
        if os.path.exists(self._file):
            self._logger.info("%s reading data from cache: %s" % (self, self._file))
            with open(self._file, "r", encoding="utf8") as f:
                self._data = f.read()
                self._logger.info("%s data read." % self)
                return True

        return False

    def get_reference(self):
        return self._reference

    def save_data(self):
        o_f = os.path.join(self._output_dir, self._output_file)
        self._logger.info("%s saving data to: %s" % (self, o_f))
        with open(os.path.join(self._output_dir, self._output_file), "w", encoding="utf8") as f:
            f.write(self._data)
            self._logger.info("%s data saved." % self)

    def set_logger(self, logger):
        self._logger = logger