'''
File:    GeoJsonDataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Import GeoJSON file into a GeoDataFrame

Created on: 2023-01-23
'''

import geopandas as gpd
from io import StringIO

from .DataConverter import DataConverter

class GeoJsonDataConverter(DataConverter):
    """
    Import GeoJSON data into a GeoDataFrame
    """

    def get_data(self):
        # retrieving data from source
        self._logger.info("%s retrieving data from %s" % (self, self._source))

        self._data = self._source.pass_data()

        return self._data != None

    def convert_data(self):
        """
        Import data into GeoDataFrame
        """
        if not self._data:
            self.get_data()

        try:
            # read json text into dataframe
            self._data = gpd.GeoDataFrame.from_file(StringIO(self._data))

            # if polygon, get centroid instead
            if (self._data.geometry.geom_type == "Polygon").any():
                self._logger.warn("%s extracting centroid from Polygon" % self)
                self._data["geometry"] = self._data["geometry"].centroid

            self._data_converted = True

            self._logger.debug("%s attributes: %s" % (self, self._data.columns))

            return False

        except:
            self._logger.error("%s data conversion failed." % self)
            return False        