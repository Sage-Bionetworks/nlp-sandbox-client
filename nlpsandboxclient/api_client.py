"""
NLP SDK client.  For developers only - interfaces with the API and
does not assume user behavior for how functions would be used. Here
are some examples on how to use this client.

    >>> from nlpsandboxclient.api_client import DataNodeApiClient
    >>> nlp = DataNodeApiClient()

    >>> # Create a new dataset
    >>> new_dataset = nlp.create_dataset(dataset_id="my-dataset")

    >>> # Create an annotation store
    >>> annotation_store = nlp.create_annotation_store(
    >>>     datasetid=annotation_store.datasetid,
    >>>     annotation_storeid="my-annotation-store"
    >>> )

    >>> # List annotation stores
    >>> annotation_stores = list(nlp.list_annotation_stores(
    >>>     datasetid=new_dataset.id
    >>> ))
"""
import os
from typing import Iterator
import urllib.parse

import requests
from synapseclient import core

from . import utils
from .datanode.models import (Annotation, AnnotationStore, Dataset,
                              FhirStore, Note, Patient)

# Default data node endpoint
DATA_NODE_HOST = "http://10.23.55.45:8080/api/v1"


def _return_rest_body(response):
    """Returns either a dictionary or a string depending on the
    'content-type' of the response.
    """
    content_type = response.headers.get('content-type', None)
    if content_type is not None and content_type.lower().strip().startswith(
            'application/json'):
        return response.json()
    return response.text


class NlpApiClient:
    """Nlp base client that does generic rest calls"""
    def __init__(self, host: str = None):
        if host is None:
            host = DATA_NODE_HOST
        self.host = host
        self._requests_session = requests.Session()

    def get_service(self) -> dict:
        """Get the health of the API

        Returns:
            Service response

        Examples:
            >>> nlp = NlpApiClient()
            >>> nlp.get_service()

        """
        return self.rest_get("/service")

    def get_ui(self, return_body: bool = False):
        """Get the ui of the API

        Args:
            return_body: Returns the response body. Default is False.

        Returns:
            Response object

        Examples:
            >>> nlp = NlpApiClient()
            >>> nlp.get_ui()
        """
        return self.rest_get("/ui", return_body=return_body)

    def rest_get(self, uri: str, endpoint: str = None,
                 return_body: bool = True):
        """Sends a HTTP GET request

        Args:
            uri: Service path
            endpoint: Service endpoint
            return_body: Returns the response body. Default is True.

        Returns:
            Response object or body

        Examples:
            >>> nlp = NlpApiClient()
            >>> nlp.get_ui()
        """
        response = self._rest_call('get', uri, None, endpoint)
        if return_body:
            return _return_rest_body(response)
        return response

    def rest_post(self, uri: str, body: str, endpoint: str = None):
        """Sends an HTTP POST request."""
        response = self._rest_call(
            'post', uri, body, endpoint
        )
        return _return_rest_body(response)

    def rest_get_paginated(self, uri, limit=10, offset=0):
        """Get pagniated rest call"""
        page_uri = core.utils._limit_and_offset(uri, limit=limit,
                                                offset=offset)
        while page_uri:
            page = self.rest_get(page_uri)
            page_uri = page['links']['next']
            # Make sure to only return the list of resources
            for key in ['limit', 'links', 'offset']:
                page.pop(key)
            # This will yield the list of resources
            # 'dict_keys' object is not subscriptable
            resouces = page.pop(list(page.keys())[0])
            for resource in resouces:
                yield resource

    def _rest_call(self, method, uri, data, endpoint, headers=None):
        """Sends HTTP requests"""
        uri = self._build_uri(uri, endpoint=endpoint)
        requests_method_fn = getattr(self._requests_session, method)
        response = requests_method_fn(uri, json=data, headers=headers)
        utils._raise_for_status(response)
        return response

    def _build_uri(self, uri, endpoint=None):
        """Returns a URI to request with."""
        if endpoint is None:
            endpoint = self.host
        # Check to see if the URI is incomplete
        # In that case, append a endpoint to the URI
        parsed_url = urllib.parse.urlparse(uri)
        if parsed_url.netloc == '':
            uri = endpoint + uri
        return uri


class DataNodeApiClient(NlpApiClient):
    """Nlp client to interact with data node"""

    def list_datasets(self) -> Iterator[Dataset]:
        """Lists all datasets

        Yields:
            Data node Dataset

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> list(nlp.list_datasets())
            [Dataset]
        """
        datasets = self.rest_get_paginated("/datasets")
        for dataset in datasets:
            # The id of the dataset is found in datasets/{dataset_id}
            # Which is the basename
            yield Dataset(id=os.path.basename(dataset['name']), **dataset)

    def get_dataset(self, dataset_id: str) -> Dataset:
        """Get a dataset

        Args:
            dataset_id: Dataset Id

        Returns:
            Data node Dataset

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> dataset = nlp.get_dataset(dataset_id="awesome-dataset")
            >>> dataset.id
            awesome-dataset
        """
        dataset = self.rest_get(f"/datasets/{dataset_id}")
        return Dataset(id=dataset_id, **dataset)

    def create_dataset(self, dataset_id: str) -> Dataset:
        """Create a dataset

        Args:
            dataset_id: Dataset Id

        Returns:
            Data node Dataset

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> dataset = nlp.create_dataset(dataset_id="awesome-dataset")
            >>> dataset.id
            awesome-dataset
        """
        dataset = self.rest_post(f"/datasets?datasetId={dataset_id}",
                                 body={})
        return Dataset(id=dataset_id, **dataset)

    def list_annotation_stores(self,
                               dataset_id: str) -> Iterator[AnnotationStore]:
        """List the annotation stores for a dataset

        Args:
            dataset_id: Dataset Id

        Yield:
            Data node annotation stores

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> annotation_stores = nlp.list_annotation_stores(
            >>>     dataset_id="awesome-dataset"
            >>> )
        """
        annotation_stores = self.rest_get_paginated(
            f"/datasets/{dataset_id}/annotationStores"
        )
        for store in annotation_stores:
            yield AnnotationStore(dataset_id=dataset_id,
                                  id=os.path.basename(store['name']),
                                  **store)

    def get_annotation_store(self, dataset_id: str,
                             annotation_store_id: str) -> AnnotationStore:
        """Get an annotation store

        Args:
            dataset_id: Dataset Id
            annotation_store_id: annotation store id

        Returns:
            Data node annotation store

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> annotation_store = nlp.get_annotation_store(
            >>>     dataset_id="awesome-dataset",
            >>>     annotation_store_id="annotation-store"
            >>> )
            >>> annotation_store.id
            annotation-store
        """
        store = self.rest_get(
            f"/datasets/{dataset_id}/annotationStores/{annotation_store_id}"
        )
        return AnnotationStore(dataset_id=dataset_id, id=annotation_store_id,
                               **store)

    def create_annotation_store(self, dataset_id: str,
                                annotation_store_id: str) -> AnnotationStore:
        """Create an annotation store

        Args:
            dataset_id: Dataset Id
            annotation_store_id: annotation store id

        Returns:
            Data node annotation store

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> annotation_store = nlp.create_annotation_store(
            >>>     dataset_id="awesome-dataset",
            >>>     annotation_store_id="my-annotation-store"
            >>> )
            >>> annotation_store.id
            my-annotation-store
        """
        store = self.rest_post(
            f"/datasets/{dataset_id}/annotationStores?"
            f"annotationStoreId={annotation_store_id}",
            body={}
        )
        return AnnotationStore(dataset_id=dataset_id, id=annotation_store_id,
                               **store)

    def list_annotations(self, dataset_id: str,
                         annotation_store_id: str) -> Iterator[Annotation]:
        """List the annotations for an annotation store

        Args:
            dataset_id: Dataset Id
            annotation_store_id: Annotation store id

        Returns:
            Data node annotations

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> annotations = nlp.list_annotations(
            >>>     dataset_id="awesome-dataset",
            >>>     annotation_store_id="my-annotation-store"
            >>> )
        """
        annotations = self.rest_get_paginated(
            f"/datasets/{dataset_id}/annotationStores/"
            f"{annotation_store_id}/annotations"
        )
        for annotation in annotations:
            yield Annotation(dataset_id=dataset_id,
                             annotation_store_id=annotation_store_id,
                             id=os.path.basename(annotation['name']),
                             **annotation)

    def get_annotation(self, dataset_id: str, annotation_store_id: str,
                       annotation_id: str) -> Annotation:
        """Get an annotation

        Args:
            dataset_id: Dataset Id
            annotation_store_id: Annotation store id
            annotation_id: Annotation id

        Returns:
            Data node Annotation

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> annotations = nlp.get_annotation(
            >>>     dataset_id="awesome-dataset",
            >>>     annotation_store_id="my-annotation-store"
            >>>     annotation_id="my-id"
            >>> )
            >>> annotations.id
            my-id
        """
        annotation = self.rest_get(
            f"/datasets/{dataset_id}/annotationStores/{annotation_store_id}/"
            f"annotations/{annotation_id}"
        )
        return Annotation(dataset_id=dataset_id,
                          annotation_store_id=annotation_store_id,
                          id=annotation_id,
                          **annotation)

    def create_annotation(self, dataset_id: str, annotation_store_id: str,
                          annotation: dict) -> Annotation:
        """Create an annotation

        Args:
            dataset_id: Dataset Id
            annotation_store_id: Annotation store id
            annotation_id: Annotation id

        Returns:
            Data node Annotation

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> annotations = nlp.create_annotation(
            >>>     dataset_id="awesome-dataset",
            >>>     annotation_store_id="my-annotation-store"
            >>>     annotation_id="my-id"
            >>> )
            >>> annotations.id
            my-id
        """
        annotation = self.rest_post(
            f"/datasets/{dataset_id}/annotationStores/"
            f"{annotation_store_id}/annotations",
            body=annotation
        )
        return Annotation(dataset_id=dataset_id,
                          annotation_store_id=annotation_store_id,
                          id=os.path.basename(annotation['name']),
                          **annotation)

    def list_fhir_stores(self, dataset_id: str) -> Iterator[FhirStore]:
        """List the FHIR stores in a dataset

        Args:
            dataset_id: Dataset Id

        Yields:
            Fhir Store

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> fhir_stores = nlp.list_fhir_stores(
            >>>     dataset_id="awesome-dataset",
            >>> )
        """
        fhir_stores = self.rest_get_paginated(
            f"/datasets/{dataset_id}/fhirStores"
        )
        for fhir_store in fhir_stores:
            yield FhirStore(dataset_id=dataset_id,
                            id=os.path.basename(fhir_store['name']),
                            **fhir_store)

    def get_fhir_store(self, dataset_id: str, fhir_store_id: str) -> FhirStore:
        """Get a FHIR store

        Args:
            dataset_id: Dataset Id
            fhir_store_id: Fhir Store Id

        Returns:
            Fhir Store

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> fhir_stores = nlp.get_fhir_store(
            >>>     dataset_id="awesome-dataset",
            >>>     fhir_store_id="my-fhir-store"
            >>> )
            >>> fhir_stores.id
            my-fhir-store
        """
        fhir_store = self.rest_get(
            f"/datasets/{dataset_id}/fhirStores/{fhir_store_id}"
        )
        return FhirStore(dataset_id=dataset_id, id=fhir_store_id,
                         **fhir_store)

    def create_fhir_store(self, dataset_id: str,
                          fhir_store_id: str) -> FhirStore:
        """Create a FHIR store

        Args:
            dataset_id: Dataset Id
            fhir_store_id: Fhir Store Id

        Returns:
            Fhir Store

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> fhir_stores = nlp.create_fhir_store(
            >>>     dataset_id="awesome-dataset",
            >>>     fhir_store_id="my-fhir-store"
            >>> )
            >>> fhir_stores.id
            my-fhir-store
        """
        fhir_store = self.rest_post(
            f"/datasets/{dataset_id}/fhirStores?fhirStoreId={fhir_store_id}",
            body={}
        )
        return FhirStore(dataset_id=dataset_id, id=fhir_store_id,
                         **fhir_store)

    def list_notes(self, dataset_id: str,
                   fhir_store_id: str) -> Iterator[Note]:
        """List clinical notes in a FHIR store

        Args:
            dataset_id: Dataset Id
            fhir_store_id: Fhir Store Id

        Yields:
            Clinical notes

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> notes = nlp.list_notes(
            >>>     dataset_id="awesome-dataset",
            >>>     fhir_store_id="my-fhir-store"
            >>> )
        """
        notes = self.rest_get_paginated(
            f"/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/Note"
        )
        for note in notes:
            yield Note(dataset_id=dataset_id, fhir_store_id=fhir_store_id,
                       **note)

    def get_note(self, dataset_id: str, fhir_store_id: str,
                 note_id: str) -> Note:
        """Get a clinical note

        Args:
            dataset_id: Dataset Id
            fhir_store_id: Fhir Store Id
            note_id: Clinical note Id

        Returns:
            Clinical note

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> note = nlp.get_note(
            >>>     dataset_id="awesome-dataset",
            >>>     fhir_store_id="my-fhir-store",
            >>>     note_id="my-note"
            >>> )
            >>> note.id
            my-note

        """
        note = self.rest_get(
            f"/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/"
            f"Note/{note_id}"
        )
        return Note(dataset_id=dataset_id, fhir_store_id=fhir_store_id, **note)

    def create_note(self, dataset_id: str, fhir_store_id: str,
                    note: dict) -> Note:
        """Create a clinical note

        Args:
            dataset_id: Dataset id
            fhir_store_id: FHIR store id
            note: Note request body

        Returns:
            Clinical note

        Examples:
            >>> nlp = DataNodeApiClient()
            >>> example_note = {
            >>>     "noteType": "loinc:LP29684-5",
            >>>     "patientId": "507f1f77bcf86cd799439011",
            >>>     "text": "This is the content of a clinical note."
            >>> }
            >>> note = nlp.create_note(
            >>>     dataset_id="awesome-dataset",
            >>>     fhir_store_id="my-fhir-store",
            >>>     note=example_note
            >>> )
            >>> note.id
            my-note
        """
        note_body = self.rest_post(
            f"/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/Note",
            body=note
        )
        return Note(dataset_id=dataset_id, fhir_store_id=fhir_store_id,
                    **note_body)

    def list_patients(self, dataset_id: str,
                      fhir_store_id: str) -> Iterator[Patient]:
        """Lists the patients in a FHIR store"""
        patients = self.rest_get_paginated(
            f"/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/Patient"
        )
        for patient in patients:
            yield Patient(dataset_id=dataset_id, fhir_store_id=fhir_store_id,
                          **patient)

    def get_patient(self, dataset_id: str, fhir_store_id: str,
                    patient_id: str) -> Patient:
        """Get a FHIR patient"""
        patient = self.rest_get(
            f"/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/"
            f"Patient/{patient_id}"
        )
        return Patient(dataset_id=dataset_id, fhir_store_id=fhir_store_id,
                       **patient)

    def create_patient(self, dataset_id: str, fhir_store_id: str,
                       patient: dict) -> Patient:
        """Create a FHIR patient"""
        patient = self.rest_post(
            f"/datasets/{dataset_id}/fhirStores/{fhir_store_id}/fhir/Patient",
            body=patient
        )
        return Patient(dataset_id=dataset_id, fhir_store_id=fhir_store_id,
                       **patient)
