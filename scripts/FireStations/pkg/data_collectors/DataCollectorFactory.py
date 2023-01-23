'''
File:    DataCollectorFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for DataCollectors

Created on: 2023-01-17
'''

from .RequestsDataCollector import RequestsDataCollector
from .EsriDataCollector     import EsriDataCollector
from .ZippedDataCollector   import ZippedDataCollector
from .FileDataCollector   import FileDataCollector

class DataCollectorFactory(object):

    def __init__(self, logger):
        self.__logger = logger

    def get_data_collector(self, cfg):
        # switch types according to configuration
        data_delivery = cfg["data_delivery"].lower().strip() 

        if data_delivery == "direct":
            instance = RequestsDataCollector(cfg)
        elif data_delivery == "esri":
            instance = EsriDataCollector(cfg)
        elif data_delivery == "zipped":
            instance = ZippedDataCollector(cfg)   
        elif data_delivery == "file":
            instance = FileDataCollector(cfg) 
        else:
            raise Exception("Unknown data delivery: %s" % data_delivery)

        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance