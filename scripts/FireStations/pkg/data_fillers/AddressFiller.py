'''
File:    AddressFiller.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for Address Fillers

Created on: 2023-01-30
'''

from .ColumnFiller import ColumnFiller

class AddressFiller(ColumnFiller):

    def __init__(self, cfg):
        super().__init__(cfg)
        self._address_pattern = cfg["address_pattern"]

    def fill_data(self):
        if self._data_filled:
            return True

        super().fill_data()
        
        self._logger.debug("%s filling Addresss %s" % (self, self._address_pattern))

        self._data[self._address_pattern["key"]] = self._data.apply(self.__build_address_from_dict, axis=1)

        self._data_filled = True

        return True

    def __build_address_from_dict(self, x):
        return self._address_pattern["pattern"] % x.to_dict()
        