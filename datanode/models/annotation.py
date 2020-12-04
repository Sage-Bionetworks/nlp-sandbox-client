# coding: utf-8

"""
    NLP Sandbox Data Node API

    The OpenAPI specification implemented by NLP Sandbox Data Nodes. # Overview A NLP Sandbox Data Node is a repository of clinical notes that implements this OpenAPI specification so that other services in the NLP Sandbox ecosystem can access them. For example, a client requests data from a Data Node before passing them as input to an NLP Tool like a Date Annotator, Person Name Annotator, etc. For the sake of benchmarking NLP Tool, a Data Node can also give access to the gold standard that the NLP Tool is expected to infer (e.g. annotations).   # noqa: E501

    The version of the OpenAPI document: 0.2.2
    Contact: thomas.schaffter@sagebionetworks.org
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from datanode.configuration import Configuration


class Annotation(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'annotation_source': 'AnnotationSource',
        'text_date_annotations': 'list[TextDateAnnotation]',
        'text_person_name_annotations': 'list[TextPersonNameAnnotation]',
        'text_physical_address_annotations': 'list[TextPhysicalAddressAnnotation]'
    }

    attribute_map = {
        'name': 'name',
        'annotation_source': 'annotationSource',
        'text_date_annotations': 'textDateAnnotations',
        'text_person_name_annotations': 'textPersonNameAnnotations',
        'text_physical_address_annotations': 'textPhysicalAddressAnnotations'
    }

    def __init__(self, name=None, annotation_source=None, text_date_annotations=None, text_person_name_annotations=None, text_physical_address_annotations=None, local_vars_configuration=None):  # noqa: E501
        """Annotation - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._annotation_source = None
        self._text_date_annotations = None
        self._text_person_name_annotations = None
        self._text_physical_address_annotations = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if annotation_source is not None:
            self.annotation_source = annotation_source
        if text_date_annotations is not None:
            self.text_date_annotations = text_date_annotations
        if text_person_name_annotations is not None:
            self.text_person_name_annotations = text_person_name_annotations
        if text_physical_address_annotations is not None:
            self.text_physical_address_annotations = text_physical_address_annotations

    @property
    def name(self):
        """Gets the name of this Annotation.  # noqa: E501

        Resource name of the annotation record, of the form datasets/{datasetId}/annotationStores/{annotationStoreId}/annotations/{annotationId}  # noqa: E501

        :return: The name of this Annotation.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Annotation.

        Resource name of the annotation record, of the form datasets/{datasetId}/annotationStores/{annotationStoreId}/annotations/{annotationId}  # noqa: E501

        :param name: The name of this Annotation.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def annotation_source(self):
        """Gets the annotation_source of this Annotation.  # noqa: E501


        :return: The annotation_source of this Annotation.  # noqa: E501
        :rtype: AnnotationSource
        """
        return self._annotation_source

    @annotation_source.setter
    def annotation_source(self, annotation_source):
        """Sets the annotation_source of this Annotation.


        :param annotation_source: The annotation_source of this Annotation.  # noqa: E501
        :type: AnnotationSource
        """

        self._annotation_source = annotation_source

    @property
    def text_date_annotations(self):
        """Gets the text_date_annotations of this Annotation.  # noqa: E501

        Date annotations in a text  # noqa: E501

        :return: The text_date_annotations of this Annotation.  # noqa: E501
        :rtype: list[TextDateAnnotation]
        """
        return self._text_date_annotations

    @text_date_annotations.setter
    def text_date_annotations(self, text_date_annotations):
        """Sets the text_date_annotations of this Annotation.

        Date annotations in a text  # noqa: E501

        :param text_date_annotations: The text_date_annotations of this Annotation.  # noqa: E501
        :type: list[TextDateAnnotation]
        """

        self._text_date_annotations = text_date_annotations

    @property
    def text_person_name_annotations(self):
        """Gets the text_person_name_annotations of this Annotation.  # noqa: E501

        Person name annotations in a text  # noqa: E501

        :return: The text_person_name_annotations of this Annotation.  # noqa: E501
        :rtype: list[TextPersonNameAnnotation]
        """
        return self._text_person_name_annotations

    @text_person_name_annotations.setter
    def text_person_name_annotations(self, text_person_name_annotations):
        """Sets the text_person_name_annotations of this Annotation.

        Person name annotations in a text  # noqa: E501

        :param text_person_name_annotations: The text_person_name_annotations of this Annotation.  # noqa: E501
        :type: list[TextPersonNameAnnotation]
        """

        self._text_person_name_annotations = text_person_name_annotations

    @property
    def text_physical_address_annotations(self):
        """Gets the text_physical_address_annotations of this Annotation.  # noqa: E501

        Physical address annotations in a text  # noqa: E501

        :return: The text_physical_address_annotations of this Annotation.  # noqa: E501
        :rtype: list[TextPhysicalAddressAnnotation]
        """
        return self._text_physical_address_annotations

    @text_physical_address_annotations.setter
    def text_physical_address_annotations(self, text_physical_address_annotations):
        """Sets the text_physical_address_annotations of this Annotation.

        Physical address annotations in a text  # noqa: E501

        :param text_physical_address_annotations: The text_physical_address_annotations of this Annotation.  # noqa: E501
        :type: list[TextPhysicalAddressAnnotation]
        """

        self._text_physical_address_annotations = text_physical_address_annotations

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Annotation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Annotation):
            return True

        return self.to_dict() != other.to_dict()
