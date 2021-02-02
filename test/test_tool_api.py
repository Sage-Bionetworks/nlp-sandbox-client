"""
    NLP Sandbox Date Annotator API

    The OpenAPI specification implemented by NLP Sandbox Annotators.   # noqa: E501

    The version of the OpenAPI document: 0.3.1
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


import unittest

import annotator
from annotator.api.tool_api import ToolApi  # noqa: E501


class TestToolApi(unittest.TestCase):
    """ToolApi unit test stubs"""

    def setUp(self):
        self.api = ToolApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_tool(self):
        """Test case for get_tool

        Get tool information  # noqa: E501
        """
        pass

    def test_get_tool_dependencies(self):
        """Test case for get_tool_dependencies

        Get tool dependencies  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
