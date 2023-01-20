'''
File:    RequestsDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for all requests-based collectors

Created on: 2023-01-18
'''

import requests, os

from .AbstractDataCollector import AbstractDataCollector

class RequestsDataCollector(AbstractDataCollector):
    """
    Base class for all requests-based collectors
    """

    def __init__(self, cfg):
        self._url = cfg['url']
        self._reference = cfg["reference"]
        self._session = requests.Session()
        self._data = None
        return

    def set_output_dir(self, d):
        self._output_dir = d

    def set_output_file(self, f):
        self._output_file = f

    def get_data(self):
        # Check if data has been read into memory
        if self._data:
            self._logger.info("%s data in memory." % self)
            return True

        # if not, check if data cache is availble
        o_f = os.path.join(self._output_dir, self._output_file)
        if os.path.exists(o_f):
            self._logger.info("%s reading data from cache: %s" % (self, o_f))
            with open(o_f, "r", encoding="utf8") as f:
                self._data = f.read()
                self._logger.info("%s data read." % self)
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

    def get_reference(self):
        return self._reference

    def save_data(self):
        o_f = os.path.join(self._output_dir, self._output_file)
        self._logger.info("%s saving data to: %s" % (self, o_f))
        with open(os.path.join(self._output_dir, self._output_file), "w", encoding="utf8") as f:
            f.write(self._data)
            self._logger.info("%s data saved." % self)

    def set_logger(self, logger):
        self._logger = logger