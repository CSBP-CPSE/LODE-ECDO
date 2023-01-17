'''
File:    CsvDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for CSV data retrieval from the web

Created on: 2023-01-17
'''

import requests, os

from .DataCollector import DataCollector

class CsvDataCollector(DataCollector):
    """
    Class for CSV data retrieval from the web
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
        self.__response = requests.get(self.__url)
        return self.__response.ok

    def get_reference(self):
        return self.__reference

    def save_data(self):
        with open(os.path.join(self.__output_dir, self.__output_file), "w", encoding="utf8") as f:
            f.write(self.__response.text)
