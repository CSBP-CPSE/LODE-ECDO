'''
File:    JsonDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for JSON data retrieval from the web

Created on: 2023-01-17
'''

from .RequestsDataCollector import RequestsDataCollector

class JsonDataCollector(RequestsDataCollector):
    """
    Base class for JSON data retrieval from the web
    """
     
