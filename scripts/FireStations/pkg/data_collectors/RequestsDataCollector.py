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
        self.__url = cfg['url']
        self.__reference = cfg["reference"]
        return

    def set_output_dir(self, d):
        self.__output_dir = d

    def set_output_file(self, f):
        self.__output_file = f

    def get_data(self):
        self.__logger.info("%s collecting data from: %s" % (self, self.__url))

        # fake user agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}
        self.__logger.debug("%s requesting data with headers: %s" % (self, headers))

        self.__response = requests.get(self.__url, headers=headers)
        if self.__response:
            self.__logger.info("%s data collected" % self)
        else:
            self.__logger.info("%s request failed with response: %s" % (self, self.__response))
        return self.__response.ok

    def get_reference(self):
        return self.__reference

    def save_data(self):
        o_f = os.path.join(self.__output_dir, self.__output_file)
        self.__logger.info("%s saving data to: %s" % (self, o_f))
        with open(os.path.join(self.__output_dir, self.__output_file), "w", encoding="utf8") as f:
            f.write(self.__response.text)
            self.__logger.info("%s data saved." % self)

    def set_logger(self, logger):
        self.__logger = logger