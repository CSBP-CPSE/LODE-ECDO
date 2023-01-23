'''
File:    RequestsDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for all requests-based collectors

Created on: 2023-01-18
'''

import requests, os

from .DataCollector import DataCollector

class RequestsDataCollector(DataCollector):
    """
    Base class for all requests-based collectors
    """

    def __init__(self, cfg):
        super().__init__(cfg)

        self._session = requests.Session()
        return

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

        self._response = self._session.get(self._url, headers=headers)
        if self._response.ok:
            self._data = self._response.text
            self._logger.info("%s data collected" % self)
        else:
            self._logger.info("%s request failed with response: %s" % (self, self._response))
        return self._response.ok