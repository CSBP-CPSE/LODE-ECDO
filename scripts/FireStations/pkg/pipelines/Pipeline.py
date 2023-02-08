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
        self._tmp_src = None
        self._sink = None

    def set_logger(self, logger):
        self._logger = logger

    def set_source(self, src):
        # keep source "in storage" until we actually connect the elements
        self._tmp_src = src

    def set_sink(self, snk):
        self._sink = snk

    def push_back(self, element):
        self._queue.append(element)

    def connect_elements(self):
        # if the pipeline has a primary external source
        # connect it to the first element of the queue
        if (self._tmp_src is not None) and (len(self._queue) > 0):
            self._logger.debug("%s connecting pipeline to external source." % self)
            self._queue[0].set_source(self._tmp_src)
        elif len(self._queue) == 0:
            # connect directly to empty self
            self._source = self._tmp_src
            self._source.set_sink(self)

        for i in range(1, len(self._queue)):
            self._queue[i].set_source(self._queue[i-1])

    def get_data(self):
        pass

    def pass_data(self):
        self._logger.info("%s [Pipeline: %s] started." % (self, self._name))
        if len(self._queue) == 0:
            # direct pull from source
            d = self._source.pass_data()
        else:
            d = self._queue[-1].pass_data()
        self._logger.info("%s [Pipeline: %s] ended." % (self, self._name))

        return d