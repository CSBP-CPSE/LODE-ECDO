'''
File:    general_checks.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: General tests before LODE release

Created on: 2023-02-01
'''

import unittest, json, os
import geopandas as gpd
from hamcrest import assert_that, not_none, contains_inanyorder

class TestSourceCoverage(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(os.path.dirname(__file__), "test_config.json"), "r") as f:
            cls.config = json.loads(f.read())

        # get list of source IDs
        with open(os.path.join(os.path.dirname(__file__), cls.config["sources"]), "r") as f:
            cls.source_ids = [i["source_id"] for i in json.loads(f.read())]

    def testSourceIDCoverage(self):
        """
        Check that all original sources are represented are represented in your dataset.
        """

        # open input file
        df = gpd.read_file(self.config["input_file"])

        # check that the data exists
        assert_that(df, not_none())

        # check that all sources are represented
        data_sids = list(df.source_id.unique())
        assert_that(data_sids, contains_inanyorder(*self.source_ids))

    @classmethod
    def tearDownClass(cls) -> None:
        pass

class TestLandCoverage(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(os.path.dirname(__file__), "test_config.json"), "r") as f:
            cls.config = json.loads(f.read())

        # list of province IDs
        # do we need strings too?
        cls.pruids = [10,11,12,13,24,35,46,47,48,59,60,61,62]

    def testProvinceIDCoverage(self):
        """
        Check that all Provinces and Territories are represented in your dataset.
        """

        # open input file
        df = gpd.read_file(self.config["input_file"])

        # check that the data exists
        assert_that(df, not_none())

        # check that all provinces are represented
        data_pruids = list(df.pruid.unique())
        assert_that(data_pruids, contains_inanyorder(*self.pruids))


    @classmethod
    def tearDownClass(cls) -> None:
        pass

if __name__ == '__main__':
    unittest.main()