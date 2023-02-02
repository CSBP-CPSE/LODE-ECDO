'''
File:    data_type_checks.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: General tests before LODE release

Created on: 2023-02-01
'''

import unittest, json, os
import geopandas as gpd
from numpy import dtype
from hamcrest import assert_that, not_none, contains_inanyorder, has_items, equal_to

class TestDataTypes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(os.path.dirname(__file__), "test_config.json"), "r") as f:
            cls.config = json.loads(f.read())

        # read dataset
        cls.data = gpd.read_file(cls.config["input_file"])
        assert_that(cls.data, not_none())

        # read schemas
        with open(os.path.join(os.path.dirname(__file__), cls.config["process_config"]), "r") as f:
            cls.schemas = json.loads(f.read())["process_schemas"]


    def testColumnsExist(self):
        """
        Check that all schema-defined columns exist in the output data.
        """    
        for schema in self.schemas:
            assert_that(self.data.columns, has_items(*schema["columns"].keys()))

    def testDataTypeConsistency(self):
        """
        Check that all output data types are consistent with the schema.
        """

        dtypes = self.data.dtypes

        for schema in self.schemas:
            for col, dt in schema["columns"].items():
                #print(col, dt, dtype(dt), dtypes[col])
                assert_that(dtype(dt).kind, equal_to(dtypes[col].kind))


    @classmethod
    def tearDownClass(cls) -> None:
        pass

if __name__ == '__main__':
    unittest.main()