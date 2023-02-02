'''
File:    DataFillerFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for DataFillers

Created on: 2023-01-20
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .DynamicColumnFiller import DynamicColumnFiller
from .StaticColumnFiller  import StaticColumnFiller 

class DataFillerFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):

        if cfg.get("fill_patterns", None):
            instance = DynamicColumnFiller(cfg)
        else:
            instance = StaticColumnFiller(cfg)
        
        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance