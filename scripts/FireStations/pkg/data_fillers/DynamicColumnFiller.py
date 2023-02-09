'''
File:    DynamicColumnFiller.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Fill columns by pattern 

Created on: 2023-01-30
'''

from .CoalesceColumnFiller import CoalesceColumnFiller

class DynamicColumnFiller(CoalesceColumnFiller):

    def __init__(self, cfg):
        super().__init__(cfg)
        self._address_patterns = cfg["fill_patterns"]

    def fill_data(self):
        if self._data_filled:
            return True

        super().fill_data()

        self._data_filled = False
        
        for pattern in self._address_patterns:
            key = pattern["key"]
            ptn = pattern["pattern"]

            self._logger.debug("%s filling column %s <- %s" % (self, key, ptn))

            self._data[key] = self._data.apply(lambda x: self.__build_address_from_dict(x, ptn), axis=1)

        self._data_filled = True

        return True

    @staticmethod
    def __build_address_from_dict(x, ptn):
        try:
            return (ptn % x.to_dict()).strip()
        except:
            return ""    