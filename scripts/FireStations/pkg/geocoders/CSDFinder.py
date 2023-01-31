'''
File:    CSDFinder.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Find CSD around given point

Created on: 2023-01-31
'''

from time import perf_counter
import geopandas as gpd

from .Geocoder import Geocoder

class CSDFinder(Geocoder):
    """
    Find CSD around given point
    """

    __csd_data = None

    def __init__(self, cfg):
        super().__init__(cfg)
        self._csd_source = cfg["csd_source"]

    @classmethod
    def __get_csd_data(cls, filename):

        if cls.__csd_data is None:
            csd_df = gpd.read_file(filename)
            csd_df = csd_df[["geometry", "CSDNAME", "CSDUID"]]
            csd_df = csd_df.to_crs("EPSG:4326")
            csd_df["CSDUID"] = csd_df["CSDUID"].astype(int)

            cls.__csd_data = csd_df
       

    def geocode_data(self):
        self._logger.info("%s initializing CSD data." % self)
        t0 = perf_counter()
        self.__get_csd_data(self._csd_source)
        self._logger.info("%s CSD data initialized in %g seconds." % (self, perf_counter() - t0))

        self._data = gpd.sjoin(self._data, self.__class__.__csd_data, how="left", predicate="within") \
            .drop(columns="index_right")

        self._data_geocoded = True
        return True