'''
File:    DummyDataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Dummy data converter for testing

Created on: 2023-01-27
'''

from .DataConverter import DataConverter

class DummyDataConverter(DataConverter):
    """
    Dummy data converter for testing
    """

    def __init__(self, cfg):
        self._source = None
        self._data = None
        self._data_converted = True

    def get_data(self):
        # retrieving data from source
        self._logger.info("%s retrieving data from %s" % (self, self._source))

        self._data = self._source.pass_data()

        return self._data != None

    def pass_data(self):
        return self._data

    def convert_data(self):
        pass