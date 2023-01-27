'''
File:    KmlDataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Import Kml data into a GeoDataFrame

Created on: 2023-01-23
'''

import geopandas as gpd
from io import StringIO
import fiona

fiona.drvsupport.supported_drivers['KML'] = 'rw'

from .DataConverter import DataConverter

class KmlDataConverter(DataConverter):
    """
    Import Kml data into a GeoDataFrame
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

            self._data = gpd.read_file(StringIO(self._data), driver='KML')
            self._data_converted = True

            self._logger.debug("%s attributes: %s" % (self, self._data.columns))

            return False

        except:
            self._logger.error("%s data conversion failed." % self)
            return False        