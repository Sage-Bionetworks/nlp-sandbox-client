"""
    NLP Sandbox Date Annotator API

    The OpenAPI specification implemented by NLP Sandbox Date Annotators. # Overview This NLP tool detects date references in the clinical note specified and returns a list of date annotations.   # noqa: E501

    The version of the OpenAPI document: 0.2.2
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import annotator
from annotator.model.text_physical_address_annotation import TextPhysicalAddressAnnotation
globals()['TextPhysicalAddressAnnotation'] = TextPhysicalAddressAnnotation
from annotator.model.text_physical_address_annotations import TextPhysicalAddressAnnotations


class TestTextPhysicalAddressAnnotations(unittest.TestCase):
    """TextPhysicalAddressAnnotations unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTextPhysicalAddressAnnotations(self):
        """Test TextPhysicalAddressAnnotations"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TextPhysicalAddressAnnotations()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()