'''
File:    CsvDataCollector.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for CSV data retrieval from the web

Created on: 2023-01-17
'''

from .RequestsDataCollector import RequestsDataCollector

class CsvDataCollector(RequestsDataCollector):
    """
    Class for CSV data retrieval from the web
    """