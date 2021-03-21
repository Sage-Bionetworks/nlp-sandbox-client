"""
    NLP Sandbox Data Node API

    # Overview  The NLP Sandbox Data Node is a repository of data used to benchmark NLP Tools like the NLP Sandbox Date Annotator and Person Name Annotator.  The resources that can be stored in this Data Node and the operations supported are listed below:  - Create and manage datasets - Create and manage FHIR stores   - Store and retrieve FHIR patient profiles   - Store and retrieve clinical   notes - Create and manage annotation stores   - Store and retrieve text annotations   # noqa: E501

    The version of the OpenAPI document: 1.0.2
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import datanode
from datanode.model.dataset import Dataset
from datanode.models import DatasetName
globals()['Dataset'] = Dataset
from datanode.model.page_of_datasets_all_of import PageOfDatasetsAllOf


class TestPageOfDatasetsAllOf(unittest.TestCase):
    """PageOfDatasetsAllOf unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPageOfDatasetsAllOf(self):
        """Test PageOfDatasetsAllOf"""
        # FIXME: construct object with mandatory attributes with example values
        # model = PageOfDatasetsAllOf()  # noqa: E501
        PageOfDatasetsAllOf(
            datasets=[Dataset(name=DatasetName("foo"))]
        )


if __name__ == '__main__':
    unittest.main()
