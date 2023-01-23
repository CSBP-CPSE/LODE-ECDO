'''
File:    DataConverterFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for DataConverters

Created on: 2023-01-23
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .FireWikiDataConverter import FireWikiDataConverter

class DataConverterFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):
        # TODO: switch types according to configuration
        #data_type = cfg["data_type"].lower().strip() 

        #if data_type == "csv":
        #    instance = CsvDataConverter(cfg)
        #elif data_type in ["json", "geojson"]:
        #    instance = JsonDataConverter(cfg)
        #elif data_type == "kml":
        #    instance = KmlDataConverter(cfg)    
        #else:
        #    raise Exception("Unknown data type: %s" % data_type)

        instance = FireWikiDataConverter(cfg)

        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance