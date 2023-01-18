'''
File:    KmlDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for KML data retrieval from the web

Created on: 2023-01-17
'''

from .RequestsDataCollector import RequestsDataCollector

class KmlDataCollector(RequestsDataCollector):
    """
    Base class for KML data retrieval from the web
    """
