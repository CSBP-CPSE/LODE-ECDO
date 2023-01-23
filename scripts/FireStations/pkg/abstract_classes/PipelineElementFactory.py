'''
File:    PipelineElementFactory.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Abstract class for Pipeline Element Factories

Created on: 2023-01-23
'''

from abc import ABC, abstractmethod

class PipelineElementFactory(ABC):

    @abstractmethod
    def get_element(self, cfg):
        pass