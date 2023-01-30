'''
File:    DataTabulatorFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Factory for DataTabulators

Created on: 2023-01-20
'''

import abstract_classes.PipelineElementFactory as PipelineElementFactory
from .DataTabulator  import DataTabulator
from .DummyDataTabulator import DummyDataTabulator

class DataTabulatorFactory(PipelineElementFactory):

    def __init__(self, logger):
        self.__logger = logger

    def get_element(self, cfg):
        # switch types according to configuration
        schema = cfg["schema"]

        if not schema:
            instance = DummyDataTabulator(cfg)
        elif type(schema) is dict:
            instance = DataTabulator(cfg)
        else:
            raise Exception("Unknown schema: %s" % (type(schema)))

        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance