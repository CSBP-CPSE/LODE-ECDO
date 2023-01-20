'''
File:    JsonDataSniffer.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for JSON data sniffing

Created on: 2023-01-20
'''

import json

from .AbstractDataSniffer import AbstractDataSniffer

class JsonDataSniffer(AbstractDataSniffer):
    """
    Class for JSON data sniffing
    """

    def __init__(self, cfg):
        self._source = None
        self._data = None
        self._json_dct = None

    def get_data(self):
        # retrieving data from source
        self._logger.info("%s retrieving data from %s" % (self, self._source))

        self._data = self._source.pass_data()

        self._json_dct = json.loads(self._data)

        return self._data != None

    def set_data_source(self, src):
        self._source = src

    def is_geojson(self):
        return self._json_dct.__class__ == dict.__class__ and \
            "type" in self._json_dct.keys() and \
            self._json_dct["type"] == "FeatureCollection"

    def get_attributes(self):
        if not self.is_geojson():
            self._logger.error("%s not GeoJSON data." % self)
            return []
        else:
            return list(self._json_dct["features"][0]["properties"].keys())