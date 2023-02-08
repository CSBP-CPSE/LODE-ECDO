'''
File:    BinarySplitter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Split data into multiple pipelines

Created on: 2023-02-06
'''

import pandas as pd
from abstract_classes.PipelineElement import PipelineElement

class _SplitterSlot(object):
    """
    Helper class for the binary splitter
    """

    def __init__(self, parent) -> None:
        self._parent = parent
        self._data = None

    def set_data(self, data):
        self._data = data

    def set_sink(self, snk):
        self._parent.set_sink(snk)

    def pass_data(self):
        # if there is no data, call parent object to create it
        if self._data is None:
            self._parent.pass_data()
        return self._data

class BinarySplitter(PipelineElement):

    def __init__(self, cfg) -> None:
        self._data = None
        self._data_split = False
        self._source = None
        self._sink = []
        self._logger = None
        self._slot_0 = _SplitterSlot(self)
        self._slot_1 = _SplitterSlot(self)
        self._slots = [self._slot_0, self._slot_1]
        self._split_condition = cfg["split_condition"]

    def set_source(self, src):
        self._source = src
        self._source.set_sink(self)

    def set_sink(self, snk):
        if len(self._sink) >= len(self._slots):
            raise Exception("%s available sinks exhausted." % self)
        self._logger.debug("%s set sink %d -> %s" % (self, len(self._sink), snk))
        self._sink.append(snk)
        
    def get_data(self):
        if self._data is None:
            self._data = self._source.pass_data()

        return True

    def set_logger(self, logger):
        self._logger = logger

    def get_slot(self, slot_id):
        if slot_id in (False, 0):
            return self._slot_0
        elif slot_id in (True, 1):
            return self._slot_1
        else:
            raise ValueError("Unknown slot id: %s" % slot_id)

    def __split_data(self):
        if self._data is None:
            self.get_data()

        # split data (is a list the most appropriate way?)

        # create temporary data frame
        temp_df = self._data[self._split_condition["column"]]

        if self._split_condition["condition"] == "equal_to":
            loc = temp_df == self._split_condition["value"]
        elif self._split_condition["condition"] == "greater_than":
            loc = temp_df > self._split_condition["value"]
        elif self._split_condition["condition"] == "greater_equal_than":
            loc = temp_df >= self._split_condition["value"]     
        else:
            raise ValueError("Unknown condition %s" % self._split_condition["condition"])     

        self._logger.debug("%s splitting data according to the condition: %s %s %s" % 
            (self, self._split_condition["column"], self._split_condition["condition"], self._split_condition["value"]))

        self._slot_0.set_data(self._data[~loc].copy())
        self._slot_1.set_data(self._data[loc].copy())

        self._data_split= True

        # delete unsplit data to save memory
        del self._data
        self._data = None

        return True

    
    def pass_data(self):
        # This method is not called directly, but delegated to children
        if not self._data_split:
            if self._data is None:
                self.get_data()

            self.__split_data()        
