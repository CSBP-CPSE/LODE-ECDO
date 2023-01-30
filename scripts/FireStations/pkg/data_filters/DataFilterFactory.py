'''
File:    DataFilterFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for DataFilters

Created on: 2023-01-20
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .DataFilter  import DataFilter
from .DummyDataFilter import DummyDataFilter

class DataFilterFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):

        if (cfg.get("filter_or", None) is not None) or \
            (cfg.get("filter_and", None) is not None) or \
            (cfg.get("filter_not", None) is not None):
            instance = DataFilter(cfg)
        else:
            instance = DummyDataFilter(cfg)
        
        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance