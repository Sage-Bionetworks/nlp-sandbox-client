"""Test client functions"""
from unittest.mock import Mock, patch

import pytest

import annotator
from annotator.api import (
    text_date_annotation_api,
    text_person_name_annotation_api,
    text_physical_address_annotation_api,
    tool_api,
)
from annotator.models import (
    License, TextDateAnnotation, TextDateAnnotationResponse, Tool, ToolType
)
import datanode
from datanode.api import (
    annotation_api, annotation_store_api,
    dataset_api, note_api,
)
from datanode.models import (
    Annotation, AnnotationName, AnnotationSource,
    AnnotationStore, AnnotationStoreName, Dataset, DatasetName,
    PageLimit, PageOfAnnotations, PageOfDatasets,
    PageOfNotes, PageOffset, PatientId, Note, NoteId,
    ResourceSource, ResponsePageMetadataLinks,
)
from datanode.rest import ApiException
from nlpsandboxclient import client


# def test_get_notes():
#     configuration = Mock()
#     api = Mock()
#     note_api_mock = Mock()
#     host = "0.0.0.0"
#     configuration = Mock()
#     note_example = PageOfNotes(
#         notes=[Note(
#             id="12344", type="foo", patient_id="pat1", text="foobarbaz"
#         )],
#         offset=0, limit=3, links=Mock(next="")
#     )

#     with patch.object(datanode, "Configuration",
#                       return_value=configuration) as config,\
#          patch.object(datanode, "ApiClient") as api_client,\
#          patch.object(datanode, "NoteApi",
#                       return_value=note_api_mock) as note_api,\
#          patch.object(note_api_mock, "list_notes",
#                       return_value=note_example) as list_notes:

#         # To mock context manager
#         api_client.return_value = api_client
#         api_client.__enter__ = Mock(return_value=api)
#         api_client.__exit__ = Mock(return_value=None)

#         notes = client.get_notes(
#             host=host,
#             dataset_id="awesome-dataset",
#             fhir_store_id="awesome-fhir-store"
#         )
#         config.assert_called_once_with(host=host)
#         api_client.assert_called_once_with(configuration)
#         note_api.assert_called_once_with(api)
#         list_notes.assert_called_once_with("awesome-dataset",
#                                            "awesome-fhir-store",
#                                            limit=10, offset=0)
#         assert notes == [{
#             'id': '12344',
#             'noteType': 'foo',
#             'patientId': 'pat1',
#             'text': 'foobarbaz',
#             'note_name': 'dataset/awesome-dataset/fhirStores/awesome-fhir-store/fhir/Note/12344'
#         }]


class TestDataNodeClient:

    def setup_method(self):
        self.configuration = datanode.Configuration()
        self.api = datanode.ApiClient()
        self.mock_api = Mock()
        self.host = "0.0.0.0"
        self.config = patch.object(datanode, "Configuration",
                                   return_value=self.configuration)
        self.api_client = patch.object(datanode, "ApiClient")
        self.dataset_id = "awesome-dataset"
        self.annotation_store_id = "annotation-store"
        self.annotation_id = "awesome-annotation"
        self.fhir_store_id = "fhir-store"
        # To mock context manager

    def test_list_notes(self):
        note_example = PageOfNotes(
            notes=[
                Note(identifier=NoteId("12344"), type="foo", patient_id=PatientId("pat1"), text="foobarbaz")
            ],
            offset=PageOffset(10),
            limit=PageLimit(10),
            links=ResponsePageMetadataLinks(next=""),
            total_results=30,
        )
        with self.config as config,\
             self.api_client as api_client,\
             patch.object(note_api, "NoteApi",
                          return_value=self.mock_api) as patch_note_api,\
             patch.object(self.mock_api, "list_notes",
                          return_value=note_example) as list_notes:

            # To mock context manager
            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            notes = list(client.list_notes(
                host=self.host,
                dataset_id=self.dataset_id,
                fhir_store_id=self.fhir_store_id
            ))
            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            patch_note_api.assert_called_once_with(self.api)
            list_notes.assert_called_once_with(self.dataset_id,
                                               self.fhir_store_id,
                                               limit=10, offset=0)
            assert notes == [{
                'identifier': '12344',
                'type': 'foo',
                'patientId': 'pat1',
                'text': 'foobarbaz',
                'note_name': f'dataset/{self.dataset_id}/fhirStores/{self.fhir_store_id}/fhir/Note/12344'
            }]

    def test_get_annotation_store__get(self):
        """Test getting of annotation store"""
        store_example = AnnotationStore(name=AnnotationStoreName("fooo"))

        with self.config as config,\
            self.api_client as api_client,\
            patch.object(annotation_store_api, "AnnotationStoreApi",
                         return_value=self.mock_api) as resource_api,\
            patch.object(self.mock_api, "get_annotation_store",
                         return_value=store_example) as get_store:

            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            store = client.get_annotation_store(
                host=self.host,
                dataset_id =self.dataset_id,
                annotation_store_id = self.fhir_store_id
            )
            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            resource_api.assert_called_once_with(self.api)
            get_store.assert_called_once_with(self.dataset_id,
                                              self.fhir_store_id)
            assert store == store_example

    def test_get_annotation_store__not_create(self):
        """Test creating of annotation store if create_if_missing is False"""
        with self.config as config,\
             self.api_client as api_client,\
             patch.object(annotation_store_api, "AnnotationStoreApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "get_annotation_store",
                          side_effect=ApiException(status=404)) as get_store,\
             pytest.raises(ApiException):

            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            client.get_annotation_store(
                host=self.host,
                dataset_id = self.dataset_id,
                annotation_store_id = self.annotation_store_id,
            )
            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            resource_api.assert_called_once_with(self.api)

    def test_get_annotation_store__create(self):
        """Test creating of annotation store if create_if_missing is True"""
        store_example = AnnotationStore(name=AnnotationStoreName("fooo"))

        with self.config as config,\
             self.api_client as api_client,\
             patch.object(annotation_store_api, "AnnotationStoreApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "get_annotation_store",
                          side_effect=ApiException(status=404)) as get_store,\
             patch.object(self.mock_api, "create_annotation_store",
                          return_value=store_example) as create_store:

            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            store = client.get_annotation_store(
                host=self.host, dataset_id = self.dataset_id,
                annotation_store_id = self.fhir_store_id,
                create_if_missing = True
            )

            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            resource_api.assert_called_once_with(self.api)
            get_store.assert_called_once_with(self.dataset_id,
                                              self.fhir_store_id)
            assert store == store_example

    def test_list_annotations(self):
        """Test listing of annotations"""
        annotation_example = PageOfAnnotations(
            annotations=[
                Annotation(
                    name=AnnotationName("12344"),
                    annotation_source=AnnotationSource(resource_source=ResourceSource(name="foo")),
                )
            ],
            offset=PageOffset(10),
            limit=PageLimit(10),
            links=ResponsePageMetadataLinks(next=""),
            total_results=30
        )

        with self.config as config,\
             self.api_client as api_client,\
             patch.object(annotation_api, "AnnotationApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "list_annotations",
                          return_value=annotation_example) as list_annotations:

            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            annotations = client.list_annotations(
                host=self.host, dataset_id = self.dataset_id,
                annotation_store_id = self.annotation_store_id
            )
            assert list(annotations) == [
                {'name': '12344', 'annotationSource': {'resourceSource': {'name': 'foo'}}}
            ]

            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            resource_api.assert_called_once_with(self.api)
            list_annotations.assert_called_once_with(
                self.dataset_id, self.annotation_store_id,
                offset=0, limit=10
            )

    def test_list_datasets(self):
        """Test listing of datasets"""
        example_datasets = PageOfDatasets(
            datasets=[
                Dataset(name=DatasetName("foo"))
            ],
            offset=PageOffset(10),
            limit=PageLimit(10),
            links=ResponsePageMetadataLinks(next=""),
            total_results=30
        )

        with self.config as config,\
             self.api_client as api_client,\
             patch.object(dataset_api, "DatasetApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "list_datasets",
                          return_value=example_datasets) as list_datasets:

            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            datasets = client.list_datasets(host=self.host)
            assert list(datasets) == [
                {'name': 'foo'}
            ]
            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            resource_api.assert_called_once_with(self.api)
            list_datasets.assert_called_once_with(limit=10, offset=0)

    def test_get_annotation(self):
        """Test getting of annotation"""
        example_annotation = Annotation(
            name=AnnotationName("12344"),
            annotation_source=AnnotationSource(resource_source=ResourceSource(name="foo")),
        )
        with self.config as config,\
             self.api_client as api_client,\
             patch.object(annotation_api, "AnnotationApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "get_annotation",
                          return_value=example_annotation) as get_annotation:

            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            annotation = client.get_annotation(
                host=self.host, dataset_id=self.dataset_id,
                annotation_store_id=self.annotation_store_id,
                annotation_id=self.annotation_id
            )
            assert annotation == example_annotation
            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            resource_api.assert_called_once_with(self.api)
            get_annotation.assert_called_once_with(
                self.dataset_id, self.annotation_store_id,
                self.annotation_id
            )

    def test__store_annotations(self):
        return_obj = Mock()
        example_annotation = Annotation(
            name=AnnotationName("12344"),
            annotation_source=AnnotationSource(resource_source=ResourceSource(name="foo")),
        )
        with self.config as config,\
             self.api_client as api_client,\
             patch.object(annotation_api, "AnnotationApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "create_annotation",
                          return_value=return_obj) as patch_store:

            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            annotation = client._store_annotation(
                host=self.host, dataset_id=self.dataset_id,
                annotation_store_id=self.annotation_store_id,
                annotation_id=self.annotation_id,
                annotation=example_annotation
            )
            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            resource_api.assert_called_once_with(self.api)
            patch_store.assert_called_once_with(
                annotation_create_request=example_annotation,
                annotation_id='awesome-annotation',
                annotation_store_id='annotation-store',
                async_req=True, dataset_id='awesome-dataset'
            )


class TestAnnotatorClient:

    def setup_method(self):
        self.configuration = annotator.Configuration()
        self.api = annotator.ApiClient()
        self.mock_api = Mock()
        self.host = "0.0.0.0"
        self.config = patch.object(annotator, "Configuration",
                                   return_value=self.configuration)
        self.api_client = patch.object(annotator, "ApiClient")
        self.example_note = {
            "identifier": "note-1",
            "type": "loinc:LP29684-5",
            "patientId": "507f1f77bcf86cd799439011",
            "text": "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott."
        }
        self.example_request = {
            "note": {
                "identifier": "note-1",
                "type": "loinc:LP29684-5",
                "patient_id": "507f1f77bcf86cd799439011",
                "text": "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott."
            }
        }
        self.date_response = TextDateAnnotationResponse(
            text_date_annotations=[
                TextDateAnnotation(start=10, length=10, text="foobar", confidence=95.5)
            ]
        )

    def test__annotate_date(self):
        """Test annotating date"""
        with patch.object(text_date_annotation_api, "TextDateAnnotationApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "create_text_date_annotations",
                          return_value="foo") as create_annotations:
            annotated = client._annotate_date(self.api, self.example_request)
            assert annotated == "foo"
            resource_api.assert_called_once_with(self.api)
            create_annotations.assert_called_once_with(
                text_date_annotation_request=self.example_request
            )

    def test__annotate_person(self):
        """Test annotating person"""
        with patch.object(text_person_name_annotation_api, "TextPersonNameAnnotationApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "create_text_person_name_annotations",
                          return_value="foo") as create_annotations:
            annotated = client._annotate_person(self.api, self.example_request)
            assert annotated == "foo"
            resource_api.assert_called_once_with(self.api)
            create_annotations.assert_called_once_with(
                text_person_name_annotation_request=self.example_request
            )

    def test__annotate_physical_address(self):
        """Test annotating physical address"""
        with patch.object(text_physical_address_annotation_api, "TextPhysicalAddressAnnotationApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "create_text_physical_address_annotations",
                          return_value="foo") as create_annotations:
            annotated = client._annotate_address(self.api, self.example_request)
            assert annotated == "foo"
            resource_api.assert_called_once_with(self.api)
            create_annotations.assert_called_once_with(
                text_physical_address_annotation_request=self.example_request
            )

    def test_annotate_note__wrong_tool_type(self):
        """Wrong tool type"""
        with pytest.raises(ValueError, match="Invalid annotator_type: foo"):
            client.annotate_note(host=self.host, note=self.example_note,
                                 tool_type="foo")

    @pytest.mark.parametrize("tool_type,tool_func", [
        ("nlpsandbox:date-annotator", "_annotate_date"),
        ("nlpsandbox:person-name-annotator", "_annotate_person"),
        ("nlpsandbox:physical-address-annotator", "_annotate_address"),
    ])
    def test_annotate_note(self, tool_type, tool_func):
        """Test annotate note"""
        with self.config as config,\
             self.api_client as api_client,\
             patch.object(client, tool_func,
                          return_value=self.date_response) as patch_annot:
            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)

            result = client.annotate_note(
                host=self.host, note=self.example_note, tool_type=tool_type
            )
            config.assert_called_once_with(host=self.host)
            api_client.assert_called_once_with(self.configuration)
            patch_annot.assert_called_once_with(self.api, self.example_request)
            assert result == {
                'textDateAnnotations': [
                    {'start': 10, 'length': 10, 'text': 'foobar', 'confidence': 95.5}
                ]
            }

    def test_get_tool(self):
        """Get tool"""
        tool_example = Tool(
            name="foo", version="1.0.0", license=License("apache-2.0"),
            repository="www.google.com", description="foobar",
            author="Bob", author_email="email@email.com", url="www.google.com",
            type=ToolType("tool"), api_version="1.0.0"
        )
        with self.config as config,\
             self.api_client as api_client,\
             patch.object(tool_api, "ToolApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "get_tool",
                          return_value=tool_example) as get_tool,\
             patch.object(client, "_get_tool_redirect",
                          return_value=tool_example.to_dict()):
            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)
            tool = client.get_tool(host=self.host)
            assert tool == tool_example

    def test_get_tool__invalid(self):
        """Tool and redirect don't match"""
        tool_example = Tool(
            name="foo", version="1.0.0", license=License("apache-2.0"),
            repository="www.google.com", description="foobar",
            author="Bob", author_email="email@email.com", url="www.google.com",
            type=ToolType("tool"), api_version="1.0.0"
        )
        with self.config as config,\
             self.api_client as api_client,\
             patch.object(tool_api, "ToolApi",
                          return_value=self.mock_api) as resource_api,\
             patch.object(self.mock_api, "get_tool",
                          return_value=tool_example) as get_tool,\
             patch.object(client, "_get_tool_redirect",
                          return_value={}),\
             pytest.raises(ValueError, match="Tool base URL must redirect*"):
            api_client.return_value = api_client
            api_client.__enter__ = Mock(return_value=self.api)
            api_client.__exit__ = Mock(return_value=None)
            tool = client.get_tool(host=self.host)
