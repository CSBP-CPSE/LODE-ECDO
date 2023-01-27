'''
File:    CSVDataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Import CSV data into a GeoDataFrame

Created on: 2023-01-23
'''

import geopandas as gpd
import pandas as pd
import re
from io import StringIO
from shapely import Point

from .DataConverter import DataConverter

class CsvDataConverter(DataConverter):
    """
    Import CSV data into a GeoDataFrame
    """

    def __init__(self, cfg):
        super().__init__(cfg)
        self._coordinates = cfg["coordinates"]

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

        if 1: #try:
            # read json text into dataframe
            df = pd.read_csv(StringIO(self._data))

            self.__set_geometry(df)

            self._data = gpd.GeoDataFrame(df, crs="epsg:4326")
            self._data_converted = True

            self._logger.debug("%s attributes: %s" % (self, self._data.columns))

            return False

        else: #except:
            self._logger.error("%s data conversion failed." % self)
            return False     

    def __set_geometry(self, df):
        # simple case: individual coordinates
        if "regex" not in self._coordinates.keys():
            x = self._coordinates['x']
            y = self._coordinates['y']

            df["geometry"] = df[[x,y]].apply(lambda a: self.__set_point(a[x], a[y]), axis=1)
        else:
            ptn = re.compile(self._coordinates["regex"])

            var   = self._coordinates["var"]
            order = self._coordinates["order"]

            df["geometry"] = df[var].apply(lambda x: self.__set_point_regex(x, ptn, order))
            

    @staticmethod
    def __set_point(x, y):
        return Point(x, y)   

    @staticmethod
    def __set_point_regex(v, ptn, order):
        match_obj = ptn.match(v)

        if match_obj:
            x = float(match_obj[order[0]])
            y = float(match_obj[order[1]])
            return Point(x, y)

        return None
