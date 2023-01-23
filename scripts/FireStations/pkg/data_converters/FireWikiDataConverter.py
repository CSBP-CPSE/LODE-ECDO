'''
File:    FireWikiDataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Convert Scrapy-JSON to GeoJSON

Created on: 2023-01-23
'''

import pandas as pd
import geopandas as gpd
from shapely import Point
from io import StringIO

from .DataConverter import DataConverter

class FireWikiDataConverter(DataConverter):
    """
    Convert Scrapy-JSON to GeoJSON
    """



    def get_data(self):
        # retrieving data from source
        self._logger.info("%s retrieving data from %s" % (self, self._source))

        self._data = self._source.pass_data()

        return self._data != None

    def convert_data(self):
        """
        Convert from Scrapy-JSON to (geo)pandas internally
        """
        if not self._data:
            self.get_data()

        try:
            # read json text into dataframe
            fd = pd.read_json(StringIO(self._data))

            fd = fd.rename(columns={"title":"fire_department_name"})

            # get individual fire stations
            fd = fd.explode("locations")

            # remove points without map data
            fd = fd[~fd.locations.isna()]

            # add data from the Google map
            fd = fd.join(fd.locations.apply(pd.Series))

            fd["title"] = fd["title"].str.strip()
            fd = fd.rename(columns={"title":"fire_station_name"}) \
                .drop(["locations", "link", "text", "icon"], axis=1)

            # check if department is is still active
            fd["active"] = fd.categories.apply(lambda x : all([not i.lower().startswith("defunct") for i in x]))
            
            # industrial vs public fire departments
            fd["industrial"] = fd.categories.apply(lambda x : any([i.lower().find("industrial") >= 0  for i in x]))
            
            # first nations fire departments
            fd["first_nations"] = fd.categories.apply(lambda x : any([i.lower().find("first nations") >= 0  for i in x]))
        
            # find province
            fd["pruid"] = fd.categories.apply(self._reverse_map_province)

            # now can drop categories
            self._logger.debug("%s field names: %s" % (self, fd.columns))
            fd.drop(["categories"], axis=1, inplace=True)

            # remove duplicates
            fd = fd.drop_duplicates(["fire_department_name", "fire_station_name", "lat", "lon"])

            # apply geometry
            fd["geometry"] = fd[["lat", "lon"]].apply(lambda x: Point(x["lon"], x["lat"]), axis=1)
            fd.drop(["lat", "lon"], axis=1, inplace=True)

            fd.reset_index()

            # save to memory
            self._data = gpd.GeoDataFrame(fd, geometry="geometry", crs="epsg:4326")

            self._data_converted = True

            return False

        except:
            self._logger.error("%s data conversion failed." % self)
            return False


    @staticmethod
    def _reverse_map_province(x):
    
        prov_dict = {   "alberta"       : 48, 
                        "columbia"      : 59,
                        "manitoba"      : 46,
                        "newfoundland"  : 10,
                        "brunswick"     : 13,
                        "scotia"        : 12,
                        "northwest"     : 61,
                        "nunavut"       : 62,
                        "prince"        : 11,
                        "ontario"       : 35,
                        "québec"        : 24,
                        "saskatchewan"  : 47,
                        "yukon"         : 60
                    }
        
        for k,v in prov_dict.items():
            if any([i.lower().find(k) >= 0 for i in x]):
                return v
        
        return -1
        
        