from .RequestsDataCollector import RequestsDataCollector
from .SeleniumDataCollector import SeleniumDataCollector
from .ZippedDataCollector   import ZippedDataCollector

class DataCollectorFactory(object):

    def __init__(self, logger):
        self.__logger = logger

    def get_data_collector(self, cfg):
        # switch types according to configuration
        data_delivery = cfg["data_delivery"].lower().strip() 

        if data_delivery == "direct":
            instance = RequestsDataCollector(cfg)
        elif data_delivery == "esri":
            instance = SeleniumDataCollector(cfg)
        elif data_delivery == "zipped":
            instance = ZippedDataCollector(cfg)    
        else:
            raise Exception("Unknown data delivery: %s" % data_delivery)

        self.__logger.info("%s created an instance of %s" % (self, instance.__class__))

        instance.set_logger(self.__logger)

        return instance