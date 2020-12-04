# coding: utf-8

"""
    NLP Sandbox Person Name Annotator API

    The OpenAPI specification implemented by NLP Sandbox Person Name Annotators. # Overview This NLP tool detects references of person names in the clinical notes given as input and returns a list of person name annotations.   # noqa: E501

    The version of the OpenAPI document: 0.2.2
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import personannotator
from personannotator.models.text_person_name_annotation_request import TextPersonNameAnnotationRequest  # noqa: E501
from personannotator.rest import ApiException

class TestTextPersonNameAnnotationRequest(unittest.TestCase):
    """TextPersonNameAnnotationRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TextPersonNameAnnotationRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = personannotator.models.text_person_name_annotation_request.TextPersonNameAnnotationRequest()  # noqa: E501
        if include_optional :
            return TextPersonNameAnnotationRequest(
                note = personannotator.models.note.Note(
                    id = '0', 
                    text = 'On 12/26/2020, Ms. Chloe Price met with Dr. Prescott.', 
                    note_type = 'loinc:LP29684-5', 
                    patient_id = '507f1f77bcf86cd799439011', )
            )
        else :
            return TextPersonNameAnnotationRequest(
        )

    def testTextPersonNameAnnotationRequest(self):
        """Test TextPersonNameAnnotationRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()