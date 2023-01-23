'''
File:    CsvDataSniffer.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for CSV data sniffing

Created on: 2023-01-20
'''

import csv

from .AbstractDataSniffer import AbstractDataSniffer

class CsvDataSniffer(AbstractDataSniffer):
    """
    Class for CSV data sniffing
    """

    def __init__(self, cfg):
        self._source = None
        self._data = None

    def get_data(self):
        # retrieving data from source
        self._logger.info("%s retrieving data from %s" % (self, self._source))

        self._data = self._source.pass_data()

        return self._data != None

    def get_attributes(self):
        r = csv.DictReader(self._data.split("\n"))
        return r.fieldnames