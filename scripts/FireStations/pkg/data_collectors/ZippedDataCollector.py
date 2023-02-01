'''
File:    ZippedDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Downloads data and extracts zip archive

Created on: 2023-01-18
'''

import zipfile, tempfile, shutil, os, io
import geopandas as gpd
from pyproj import CRS

from .RequestsDataCollector import RequestsDataCollector

class ZippedDataCollector(RequestsDataCollector):
    """
    Downloads data and extracts zip archive
    """
    __target_crs = CRS("epsg:4326")

    def __init__(self, cfg):
        super().__init__(cfg)
        if cfg.get("source_crs", None) is not None:
            self._source_crs = CRS(cfg.get("source_crs", None))

        # need file type to do search inside zipfile
        self._data_type = cfg['data_type']

    def get_data(self):
        # Check if data has been read into memory
        if self.check_data_loaded():
            return True

        # if not, check if data cache is availble
        if self.retrieve_cached_data():
            return True

        self._logger.info("%s collecting data from: %s" % (self, self._url))

        # fake user agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}
        self._logger.debug("%s requesting data with headers: %s" % (self, headers))

        # get binary data
        self._response = self._session.get(self._url, headers=headers)
        if self._response.ok:
            self._logger.info("%s data collected" % self)
        else:
            self._logger.info("%s request failed with response: %s" % (self, self._response))
            return self._response.ok

        # create a temporary folder to copy the data
        tempdir = tempfile.mkdtemp()
        self._logger.debug("%s created temporary folder: %s" % (self, tempdir))

        # copy the data to a file 
        zipf = zipfile.ZipFile(io.BytesIO(self._response.content))

        target_file = None
        for i,j in enumerate(zipf.namelist()):
            self._logger.debug("%s file content [%d]: %s" % (self, i, j))
            if j.lower().strip().endswith(self._data_type):
                target_file = j
                self._logger.debug("%s found target file: %s" % (self, target_file))
                break

        if not target_file:
            self._logger.error("%s target %s file not found" % (self, self._data_type))
            shutil.rmtree(tempdir)
            return False

        # Extract data
        zipf.extractall(path=tempdir)

        # If data is shapefile, then auxiliary files must be read too
        if self._data_type == "shp":
            df = gpd.read_file(os.path.join(tempdir, target_file))

            if df.crs is None:
                self._logger.info("%s data has no CRS, setting to %s" % (self, self._source_crs))
                df = df.set_crs(self._source_crs)
            
            if df.crs != self.__target_crs:
                self._logger.info("%s data has CRS: %s, converting to %s" % (self, df.crs, self.__target_crs))
                df = df.to_crs(self.__target_crs) 

            self._data = df.to_json()
        else:
            with open(os.path.join(tempdir, target_file), "r") as f:
                self._data = f.read()

        # cleanup
        shutil.rmtree(tempdir)

        return True


