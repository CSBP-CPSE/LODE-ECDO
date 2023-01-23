'''
File:    KmlDataSniffer.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Class for KML data sniffing

Created on: 2023-01-20
'''

from pykml import parser

from .AbstractDataSniffer import AbstractDataSniffer

class KmlDataSniffer(AbstractDataSniffer):
    """
    Class for KML data sniffing
    """

    def __init__(self, cfg):
        self._source = None
        self._data = None
        self._root = None

    def get_data(self):
        # retrieving data from source
        self._logger.info("%s retrieving data from %s" % (self, self._source))

        self._data = self._source.pass_data()

        # parser needs bytestream to work
        # https://stackoverflow.com/a/38244227
        xml = bytes(bytearray(self._data, encoding='utf-8'))
        self._root = parser.fromstring(xml)

        return self._data != None

    def get_attributes(self):
        # generic tag namespace
        ns = self._root.nsmap[None]
        # get children tags of first data point
        # TODO: sanitize
        return [i.tag for i in self._root.Document.Folder.find("..//{%s}Placemark" % ns).getchildren()]