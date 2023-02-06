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

    def pass_data(self):
        return [p.pass_data() for p in self._pipelines]

    