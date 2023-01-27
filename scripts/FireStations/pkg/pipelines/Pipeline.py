'''
File:    Pipeline.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Base class for pipelines

Created on: 2023-01-27
'''

from collections import deque

class Pipeline(object):
    """
    Base class for pipelines
    """

    def __init__(self, name, logger) -> None:
        self._queue  = deque()
        self._name   = name
        self._logger = logger

    def push_back(self, element):
        self._queue.append(element)

    def connect_elements(self):
        for i in range(1, len(self._queue)):
            self._queue[i].set_source(self._queue[i-1])

    def run(self):
        self._logger.info("%s [Pipeline: %s] started." % (self, self._name))
        self._queue[-1].pass_data()
        self._logger.info("%s [Pipeline: %s] ended." % (self, self._name))