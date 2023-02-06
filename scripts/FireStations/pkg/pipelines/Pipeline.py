'''
File:    Pipeline.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for pipelines

Created on: 2023-01-27
'''

from collections import deque
from abstract_classes.PipelineElement import PipelineElement

class Pipeline(PipelineElement):
    """
    Base class for pipelines
    """

    def __init__(self, name) -> None:
        self._queue  = deque()
        self._name   = name
        self._source = None 

    def set_logger(self, logger):
        self._logger = logger

    def set_source(self, src):
        self._source = src

    def push_back(self, element):
        self._queue.append(element)

    def connect_elements(self):
        # if the pipeline has a primary external source
        # connect it to the first element of the queue
        if self._source is not None:
            self._logger.debug("%s connecting pipeline to external source." % self)
            self._queue[0].set_source(self._source)


        for i in range(1, len(self._queue)):
            self._queue[i].set_source(self._queue[i-1])

    def get_data(self):
        pass

    def pass_data(self):
        self._logger.info("%s [Pipeline: %s] started." % (self, self._name))
        d = self._queue[-1].pass_data()
        self._logger.info("%s [Pipeline: %s] ended." % (self, self._name))

        return d