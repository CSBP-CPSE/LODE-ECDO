'''
File:    PipelineCollection.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: Collection of Pipelines running "in parallel"

Created on: 2023-02-06
'''

from collections import deque

class PipelineCollection(object):
    """
    Collection of Pipelines running "in parallel"
    """

    def __init__(self) -> None:
        self._pipelines  = deque()

    def add_pipeline(self, pipeline):
        self._pipelines.append(pipeline)

    def set_source(self, source):
        if type(source) != list or (type(source) == list and len(source) == 1):
            for p in self._pipelines:
                p.set_source(source)
        else:
            for s, p in zip(source, self._pipelines):
                p.set_source(s)

    def set_sink(self, sink):
        if type(sink) != list or (type(sink) == list and len(sink) == 1):
            for p in self._pipelines:
                p.set_sink(sink)
        else:
            for s, p in zip(sink, self._pipelines):
                p.set_sink(s)

    def broadcast_connect(self):
        for p in self._pipelines:
            p.connect_elements()

    def pass_data(self):
        return [p.pass_data() for p in self._pipelines]

    