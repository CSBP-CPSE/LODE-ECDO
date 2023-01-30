'''
File:    SaskatoonFireDataConverter.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Import Saskatoon KML data

Created on: 2023-01-30
'''

from bs4 import BeautifulSoup
from pandas import Series
from .KmlDataConverter import KmlDataConverter

class SaskatoonFireDataConverter(KmlDataConverter):
    """
    Import Kml data into a GeoDataFrame
    """

    def convert_data(self):
        self._logger.info("%s in convert_data()" % self)

        super().convert_data()

        self._data_converted = False

        # parse description table into dataframe
        desc_df = self._data.Description \
            .apply(self.__parse_description_table) \
            .apply(Series)

        self._data = self._data.join(desc_df)

        self._logger.debug("%s attributes: %s" % (self, self._data.columns))

        self._data_converted = True

        return True
        
    @staticmethod
    def __parse_description_table(x):
        soup = BeautifulSoup(x, 'html.parser')

        dct = {}
        
        for i in soup.find_all('tr'):
            for j in i.find_all('tr'):
                cells = [k.text for k in j.find_all('td')]
                dct.update({cells[0]: cells[1]})

        return dct

