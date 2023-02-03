'''
File:    DeduplicatorFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for Deduplicators

Created on: 2023-02-03
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .GeographicDeduplicator import GeographicDeduplicator

class DeduplicatorFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):

        #if (cfg.get("csd_source", None) is not None):
        #    instance = CSDFinder(cfg)
        #if 1: #else:
        instance = GeographicDeduplicator(cfg)
        
        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance