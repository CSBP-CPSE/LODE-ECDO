'''
File:    DataConverterFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for DataConverters

Created on: 2023-01-23
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .FireWikiDataConverter import FireWikiDataConverter
from .GeoJsonDataConverter import GeoJsonDataConverter
from .DummyDataConverter import DummyDataConverter
from .CsvDataConverter import CsvDataConverter
from .KmlDataConverter import KmlDataConverter

class DataConverterFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):

        data_type = cfg["data_type"].lower().strip() 

        if data_type == "csv":
            instance = CsvDataConverter(cfg)
        elif data_type == "geojson":
            instance = GeoJsonDataConverter(cfg)
        elif data_type == "kml":
            instance = KmlDataConverter(cfg)    
        else:
            instance = DummyDataConverter(cfg)
        #    raise Exception("Unknown data type: %s" % data_type)

        #instance = FireWikiDataConverter(cfg)

        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        # set cache path and file
        instance.set_cache_dir(cfg["cache_dir"])
        instance.set_cache_file("data_conversion_sid%(source_id)0.3d_%(area)s.geojson" % cfg)

        return instance