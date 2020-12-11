# coding: utf-8

"""
    NLP Sandbox Data Node API

    The OpenAPI specification implemented by NLP Sandbox Data Nodes. # Overview A NLP Sandbox Data Node is a repository of clinical notes that implements this OpenAPI specification so that other services in the NLP Sandbox ecosystem can access them. For example, a client requests data from a Data Node before passing them as input to an NLP Tool like a Date Annotator, Person Name Annotator, etc. For the sake of benchmarking NLP Tool, a Data Node can also give access to the gold standard that the NLP Tool is expected to infer (e.g. annotations).   # noqa: E501

    The version of the OpenAPI document: 0.2.2
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import datanode
from datanode.api.dataset_api import DatasetApi  # noqa: E501
from datanode.rest import ApiException


class TestDatasetApi(unittest.TestCase):
    """DatasetApi unit test stubs"""

    def setUp(self):
        self.api = datanode.api.dataset_api.DatasetApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_dataset(self):
        """Test case for create_dataset

        Create a dataset  # noqa: E501
        """
        pass

    def test_delete_dataset(self):
        """Test case for delete_dataset

        Delete a dataset by ID  # noqa: E501
        """
        pass

    def test_get_dataset(self):
        """Test case for get_dataset

        Get a dataset by ID  # noqa: E501
        """
        pass

    def test_list_datasets(self):
        """Test case for list_datasets

        Get all datasets  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()