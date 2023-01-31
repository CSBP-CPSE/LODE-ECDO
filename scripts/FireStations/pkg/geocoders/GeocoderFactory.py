'''
File:    GeocoderFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for Geocoders

Created on: 2023-01-31
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .CSDFinder import CSDFinder
from .DummyGeoCoder import DummyGeocoder

class GeocoderFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):

        if (cfg.get("csd_source", None) is not None):
            instance = CSDFinder(cfg)
        else:
            instance = DummyGeocoder(cfg)
        
        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance