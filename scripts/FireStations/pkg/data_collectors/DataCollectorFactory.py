from .CsvDataCollector import CsvDataCollector
from .JsonDataCollector import JsonDataCollector
from .KmlDataCollector import KmlDataCollector
from .SeleniumDataCollector import SeleniumDataCollector

class DataCollectorFactory(object):

    @staticmethod
    def get_data_collector(cfg):
        # switch types according to configuration
        data_type = cfg["data_type"].lower().strip() 

        if data_type== "csv":
            return CsvDataCollector(cfg)
        elif data_type== "kml":
            return KmlDataCollector(cfg)
        elif data_type== "esri":
            return SeleniumDataCollector(cfg)
        elif data_type in ["json", "geojson", "topojson"]:
            return JsonDataCollector(cfg)
        else:
            raise Exception("Unknown data type: %s" % data_type)