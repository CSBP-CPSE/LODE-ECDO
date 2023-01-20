'''
File:    DataSnifferFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for DataSniffers

Created on: 2023-01-20
'''

from .CsvDataSniffer  import CsvDataSniffer
from .JsonDataSniffer import JsonDataSniffer
from .KmlDataSniffer  import KmlDataSniffer

class DataSnifferFactory(object):

    def __init__(self, logger):
        self.__logger = logger

    def get_data_sniffer(self, cfg):
        # switch types according to configuration
        data_type = cfg["data_type"].lower().strip() 

        if data_type == "csv":
            instance = CsvDataSniffer(cfg)
        elif data_type in ["json", "geojson"]:
            instance = JsonDataSniffer(cfg)
        elif data_type == "kml":
            instance = KmlDataSniffer(cfg)    
        else:
            raise Exception("Unknown data type: %s" % data_type)

        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance