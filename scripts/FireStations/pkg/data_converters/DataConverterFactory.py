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
from .SaskatoonFireDataConverter import SaskatoonFireDataConverter

class DataConverterFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):

        data_type = cfg["data_type"].lower().strip() 
        special_converter = cfg.get("special_converter", None)

        # TODO: find a better way to instantiate "special" converters?
        if special_converter is not None:
            if special_converter == "firewiki":
                instance = FireWikiDataConverter(cfg)
            elif special_converter == "saskatoon_fire":
                instance = SaskatoonFireDataConverter(cfg)
            else:
                raise Exception("Unknown converter type: %s" % special_converter)
        else:
            if data_type == "csv":
                instance = CsvDataConverter(cfg)
            elif data_type in ["json", "geojson", "shp"]:
                instance = GeoJsonDataConverter(cfg)
            elif data_type == "kml":
                instance = KmlDataConverter(cfg)    
            else:
                instance = DummyDataConverter(cfg)

        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        # set cache path and file
        instance.set_cache_dir(cfg["cache_dir"])
        instance.set_cache_file("data_conversion_sid%(source_id)0.3d_%(area)s.geojson" % cfg)

        return instance