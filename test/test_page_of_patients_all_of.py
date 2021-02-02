"""
    NLP Sandbox Data Node API

    The OpenAPI specification implemented by NLP Sandbox Data Nodes. # Overview A NLP Sandbox Data Node is a repository of clinical notes that implements this OpenAPI specification so that other services in the NLP Sandbox ecosystem can access them. For example, a client requests data from a Data Node before passing them as input to an NLP Tool like a Date Annotator, Person Name Annotator, etc. For the sake of benchmarking NLP Tool, a Data Node can also give access to the gold standard that the NLP Tool is expected to infer (e.g. annotations).   # noqa: E501

    The version of the OpenAPI document: 0.3.1
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import datanode
from datanode.model.patient import Patient
globals()['Patient'] = Patient
from datanode.model.page_of_patients_all_of import PageOfPatientsAllOf


class TestPageOfPatientsAllOf(unittest.TestCase):
    """PageOfPatientsAllOf unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPageOfPatientsAllOf(self):
        """Test PageOfPatientsAllOf"""
        # FIXME: construct object with mandatory attributes with example values
        # model = PageOfPatientsAllOf()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
