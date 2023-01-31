'''
File:    DummyGeocoder.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Dummy Geocoder

Created on: 2023-01-31
'''

from .Geocoder import Geocoder

class DummyGeocoder(Geocoder):
    """
    Dummy Geocoder
    """

    def __init__(self, cfg):
        super().__init__(cfg)
        self._data_geocoded = True

    def geocode_data(self):
        self._data_geocoded = True