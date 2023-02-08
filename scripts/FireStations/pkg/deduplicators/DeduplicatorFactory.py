'''
File:    DeduplicatorFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for Deduplicators

Created on: 2023-02-03
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .GeographicComparison import GeographicComparison
from .StringComparison import StringComparison

class DeduplicatorFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):

        instance = None

        dd_cfg = cfg.get("dedupe_config", None)

        if dd_cfg is not None:
            if dd_cfg["type"].lower() != "string":
                instance = GeographicComparison(dd_cfg)
            else:
                instance = StringComparison(dd_cfg)
            
            self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

            instance.set_logger(self.__logger)

        return instance