'''
File:    DataTabulator.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for data tabulators

Created on: 2023-01-30
'''

import abstract_classes.PipelineElement as PipelineElement

class DataTabulator(PipelineElement):

    def __init__(self, cfg):
        self._source = None
        self._data = None
        self._schema = cfg["schema"]
        self._process_schema = cfg["process_schemas"]
        self._data_tabulated = False

    def set_source(self, src):
        self._source = src

    def get_data(self):
        self._data = self._source.pass_data()

    def pass_data(self):
        if self._data is None:
            self.get_data()
        if self._data is not None:
            self.tabulate()
        return self._data

    def tabulate(self):
        if self._data_tabulated:
            return True
        
        # columns defined in the process schema must be retained and renamed
        # all other columns must be dropped
        rename_dict = {}

        for schema in self._process_schema:
            if self._schema:
                for k, v in self._schema.items():
                    if k == schema["schema_name"]:
                        rename_dict.update(dict([(j,i) for i,j in v.items()]))

        self._logger.debug("%s rename columns: %s" % (self, rename_dict))

        self._data.rename(columns=rename_dict, inplace=True)

        drop_columns = [i for i in self._data.columns if i not in rename_dict.values()]
        drop_columns.remove("geometry")

        self._logger.debug("%s dropping columns: %s" % (self, drop_columns))
        self._data.drop(columns=drop_columns, inplace=True)

        self._data_tabulated = True

        return True

    def set_logger(self, logger):
        self._logger = logger
