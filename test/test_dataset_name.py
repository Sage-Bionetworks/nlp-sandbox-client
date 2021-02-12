"""
    NLP Sandbox Data Node API

    # Overview The NLP Sandbox Data Node is a repository of data used to benchmark NLP Tools like the NLP Sandbox Date Annotator and Person Name Annotator. The resources that can be stored in this Data Node and the operations supported are listed below: - Create and manage datasets - Create and manage FHIR stores   - Store and retrieve FHIR patient profiles   - Store and retrieve clinical notes - Create and manage annotation stores   - Store and retrieve text annotations   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import datanode
from datanode.model.dataset_name import DatasetName


class TestDatasetName(unittest.TestCase):
    """DatasetName unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDatasetName(self):
        """Test DatasetName"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DatasetName()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
