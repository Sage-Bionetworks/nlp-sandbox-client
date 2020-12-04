# coding: utf-8

"""
    NLP Sandbox Physical Address Annotator API

    The OpenAPI specification implemented by NLP Sandbox Physical Address Annotators. # Overview This NLP tool detects references of physical addresses in the clinical notes given as input and returns a list of physical address annotations.   # noqa: E501

    The version of the OpenAPI document: 0.2.2
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import addressannotator
from addressannotator.models.text_physical_address_annotations import TextPhysicalAddressAnnotations  # noqa: E501
from addressannotator.rest import ApiException

class TestTextPhysicalAddressAnnotations(unittest.TestCase):
    """TextPhysicalAddressAnnotations unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TextPhysicalAddressAnnotations
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = addressannotator.models.text_physical_address_annotations.TextPhysicalAddressAnnotations()  # noqa: E501
        if include_optional :
            return TextPhysicalAddressAnnotations(
                text_physical_address_annotations = [
                    {"start":42,"length":11,"text":"Seattle","addressType":"city"}
                    ]
            )
        else :
            return TextPhysicalAddressAnnotations(
        )

    def testTextPhysicalAddressAnnotations(self):
        """Test TextPhysicalAddressAnnotations"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()