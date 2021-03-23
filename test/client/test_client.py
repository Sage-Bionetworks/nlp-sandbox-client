"""Test client functions"""
from unittest.mock import Mock, patch

import pytest

import annotator
from annotator.api import text_date_annotation_api
import datanode
from datanode.api import note_api, annotation_api, annotation_store_api
from datanode.models import (
    Annotation, AnnotationName, AnnotationSource,
    AnnotationStore, AnnotationStoreName,
    PageLimit, PageOfAnnotations,
    PageOfNotes, PageOffset, PatientId, Note, NoteId,
    ResourceSource,
    ResponsePageMetadataLinks,
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
#             id="12344", note_type="foo", patient_id="pat1", text="foobarbaz"
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
        """Test creating of annotation store if create_if_missing is True"""
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


class TestAnnotatorClient:

    def setup_method(self):
        self.configuration = annotator.Configuration()
        self.api = annotator.ApiClient()
        self.mock_api = Mock()
        self.host = "0.0.0.0"
        self.config = patch.object(annotator, "Configuration",
                                   return_value=self.configuration)
        self.api_client = patch.object(annotator, "ApiClient")
        self.example_request = {
            "note": {
                "identifier": "note-1",
                "note_type": "loinc:LP29684-5",
                "patient_id": "507f1f77bcf86cd799439011",
                "text": "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott."
            }
        }

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

    # def test__annotate_person(self):
    #     """Test annotating person"""
    #     with patch.object(text_date_annotation_api, "TextDateAnnotationApi",
    #                       return_value=self.mock_api) as resource_api,\
    #          patch.object(self.mock_api, "create_text_date_annotations",
    #                       return_value="foo") as list_annotations:
    #         annotated = client._annotate_date(self.api, self.example_request)
    #         assert annotated == "foo"

    # def test__annotate_physical_address(self):
    #     """Test annotating physical address"""
    #     with patch.object(text_date_annotation_api, "TextDateAnnotationApi",
    #                       return_value=self.mock_api) as resource_api,\
    #          patch.object(self.mock_api, "create_text_date_annotations",
    #                       return_value="foo") as list_annotations:
    #         annotated = client._annotate_date(self.api, self.example_request)
    #         assert annotated == "foo"