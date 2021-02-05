"""NLP data node client that interacts with the SDK datanodeclient"""
from typing import List, Iterator

import datanode
from datanode.api import annotation_store_api, annotation_api, note_api
from datanode.models import Annotation, AnnotationStore
import annotator
from annotator.api import (text_date_annotation_api,
                           text_person_name_annotation_api,
                           text_physical_address_annotation_api,
                           tool_api)
from annotator.models import Tool
from . import utils

DATA_NODE_HOST = "http://10.23.54.142/api/v1"


def list_notes(host: str, dataset_id: str, fhir_store_id: str) -> List[dict]:
    """Get all clinical notes for a dataset

    Args:
        host: Data node host IP
        dataset_id: Dataset Id
        fhir_store_id: FHIR store Id

    Yields:
        list of clinical notes.

    Examples:
        >>> notes = get_notes(host="0.0.0.0/api/v1",
        >>>                   dataset_id="awesome-dataset",
        >>>                   fhir_store_id="awesome-fhir-store")
        >>> list(notes)[0]
        {
            "id": "noteid",
            "noteType": "",
            "patientId": "patient_id",
            "text": "Example text",
            "note_name": "dataset/awesome-dataset/fhirStores/awesome-fhirstore/fhir/Note/noteid"
        }
    """
    configuration = datanode.Configuration(host=host)
    offset = 0
    limit = 10
    with datanode.ApiClient(configuration) as api_client:
        note_instance = note_api.NoteApi(api_client)
        # Obtain all clinical notes
        next_page = True
        while next_page:
            notes = note_instance.list_notes(dataset_id, fhir_store_id,
                                             offset=offset, limit=limit)
            # change from snake case to camel case
            sanitized_notes = api_client.sanitize_for_serialization(
                notes.notes
            )
            for note in sanitized_notes:
                note["note_name"] = f"dataset/{dataset_id}/fhirStores/{fhir_store_id}/fhir/Note/{note['id']}"
                yield note
            next_page = notes.links.next
            offset += limit


def get_annotation_store(host: str, dataset_id: str,
                         annotation_store_id: str,
                         create_if_missing: bool = False) -> AnnotationStore:
    """Creates an annotation store

    Args:
        host: Data node host IP
        dataset_id: Dataset Id
        annotation_store_id: Annotation store Id
        create_if_missing: Creates annotation store if the resource
                           doesn't exist

    Returns:
        Data node Annotation Store object

    Examples:
        >>> annotation = create_annotation_store(
        >>>     host="0.0.0.0/api/v1", dataset_id="awesome-dataset",
        >>>     annotation_store_id="awesome-annotation-store"
        >>> )

    """
    configuration = datanode.Configuration(host=host)
    with datanode.ApiClient(configuration) as api_client:
        annot_store_instance = annotation_store_api.AnnotationStoreApi(
            api_client
        )
        try:
            # get the annotation store
            annotation_store_obj = annot_store_instance.get_annotation_store(
                dataset_id, annotation_store_id
            )
        except datanode.rest.ApiException as err:
            if err.status == 404 and create_if_missing:
                annotation_store_obj = annot_store_instance.create_annotation_store(
                    dataset_id, annotation_store_id, body={}
                )
            else:
                raise err
    return annotation_store_obj


def store_annotation(host: str, dataset_id: str, annotation_store_id: str,
                     annotation: dict) -> Annotation:
    """Store annotation

    Args:
        host: Data node host IP
        dataset_id: Dataset Id
        annotation_store_id: Annotation store Id
        annotation: Annotation dict

    Returns:
        Data node Annotation object

    Examples:
        >>> example_annotation = {
        >>>     "annotationSource": {
        >>>         "resourceSource": {
        >>>             "name": "name"
        >>>         }
        >>>     },
        >>>     "textDateAnnotations": [
        >>>         {
        >>>             "dateFormat": "MM/DD/YYYY",
        >>>             "length": 10,
        >>>             "start": 42,
        >>>             "text": "10/26/2020"
        >>>         },
        >>>         {
        >>>             "dateFormat": "MM/DD/YYYY",
        >>>             "length": 10,
        >>>             "start": 42,
        >>>             "text": "10/26/2020"
        >>>         }
        >>>     ],
        >>>     "textPersonNameAnnotations": [],
        >>>     "textPhysicalAddressAnnotations": []
        >>> }
        >>> annotation = store_annotation(host="0.0.0.0/api/v1",
        >>>                               dataset_id="awesome-dataset",
        >>>                               annotation_store_id="awesome-annotation-store",
        >>>                               annotation_create_request=example_annotation)

    """

    configuration = datanode.Configuration(host=host)
    with datanode.ApiClient(configuration) as api_client:
        annotation_instance = annotation_api.AnnotationApi(api_client)
        new_annotation = utils.change_keys(annotation,
                                           utils.camelcase_to_snakecase)
        annotation_obj = annotation_instance.create_annotation(
            dataset_id=dataset_id,
            annotation_store_id=annotation_store_id,
            annotation_create_request=new_annotation,
            async_req=True
        )
    return annotation_obj.get()


def list_annotations(host: str, dataset_id: str,
                     annotation_store_id: str) -> Iterator[dict]:
    """List annotations

    Args:
        host: Data node host IP
        dataset_id: Dataset Id
        annotation_store_id: Annotation store Id

    Yields:
        Data node annotation objects

    Examples:
        >>> annotations = get_annotations(host="0.0.0.0/api/v1",
        >>>                               dataset_id="awesome-dataset",
        >>>                               annotation_store_id="awesome-annotation-store")

    """
    configuration = datanode.Configuration(host=host)
    offset = 0
    limit = 10
    with datanode.ApiClient(configuration) as api_client:
        annotation_instance = annotation_api.AnnotationApi(api_client)
        next_page = True
        while next_page:
            annotations = annotation_instance.list_annotations(
                dataset_id, annotation_store_id,
                offset=offset, limit=limit
            )
            # change from snake case to camel case
            sanitized_annotations = api_client.sanitize_for_serialization(
                annotations.annotations
            )
            for annotation in sanitized_annotations:
                yield annotation
            next_page = annotations.links.next
            offset += limit


def _annotate_person(api_client, note: dict) -> dict:
    """Annotate notes with date

    Args:
        host: Data node host IP
        note: Clinical note

    Yields:
        Annotated notes

    Examples:
        >>> example_note = {
        >>>    "note": {
        >>>        "noteType": "loinc:LP29684-5",
        >>>        "patientId": "507f1f77bcf86cd799439011",
        >>>        "text": "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott."
        >>>    }
        >>> }
        >>> host = "0.0.0.0:8080/api/v1"
        >>> configuration = annotator.Configuration(host=host)
        >>> with annotator.ApiClient(configuration) as api_client:
        >>>     annotations = _annotate_person(api_client=api_client,
        >>>                                    note=example_note)

    """
    # host = "http://10.23.55.45:9000/api/v1"
    api_instance = text_person_name_annotation_api.TextPersonNameAnnotationApi(api_client)
    annotations = api_instance.create_text_person_name_annotations(
        text_person_name_annotation_request=note
    )
    return annotations


def _annotate_address(api_client, note: dict) -> dict:
    """Annotate notes with date

    Args:
        host: Data node host IP
        note: Clinical note

    Yields:
        Annotated notes

    Examples:
        >>> example_note = {
        >>>    "note": {
        >>>        "noteType": "loinc:LP29684-5",
        >>>        "patientId": "507f1f77bcf86cd799439011",
        >>>        "text": "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott in Seattle."
        >>>    }
        >>> }
        >>> host = "0.0.0.0:8080/api/v1"
        >>> configuration = annotator.Configuration(host=host)
        >>> with annotator.ApiClient(configuration) as api_client:
        >>>     annotations = _annotate_address(api_client=api_client,
        >>>                                     note=example_note)

    """
    # host = "http://10.23.55.45:9000/api/v1"
    api_instance = text_physical_address_annotation_api.TextPhysicalAddressAnnotationApi(api_client)
    annotations = api_instance.create_text_physical_address_annotations(
        text_physical_address_annotation_request=note
    )
    return annotations


def _annotate_date(api_client, note: dict) -> dict:
    """Annotate notes with date

    Args:
        host: Data node host IP
        note: Clinical note

    Yields:
        Annotated notes

    Examples:
        >>> example_note = {
        >>>    "note": {
        >>>        "noteType": "loinc:LP29684-5",
        >>>        "patientId": "507f1f77bcf86cd799439011",
        >>>        "text": "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott."
        >>>    }
        >>> }
        >>> host = "0.0.0.0:8080/api/v1"
        >>> configuration = annotator.Configuration(host=host)
        >>> with annotator.ApiClient(configuration) as api_client:
        >>>     annotations = _annotate_date(api_client=api_client,
        >>>                                  note=example_note)

    """
    # host = "http://10.23.55.45:9000/api/v1"
    api_instance = text_date_annotation_api.TextDateAnnotationApi(api_client)
    annotations = api_instance.create_text_date_annotations(
        text_date_annotation_request=note
    )
    return annotations


def annotate_note(host: str, note: dict, annotator_type: str) -> dict:
    """Annotate notes

    Args:
        host: Data node host IP
        note: Clinical note
        annotator_type: Type of annotator

    Yields:
        Annotated notes

    Examples:
        >>> example_note = {
        >>>    "note": {
        >>>        "noteType": "loinc:LP29684-5",
        >>>        "patientId": "507f1f77bcf86cd799439011",
        >>>        "text": "On 12/26/2020, Ms. Chloe Price met with Dr. Prescott."
        >>>    }
        >>> }
        >>> annotations = annotate_note(host="0.0.0.0/api/v1",
        >>>                             note=example_note,
        >>>                             annotator_type="date")

    """
    # host = "http://10.23.55.45:9000/api/v1"
    configuration = annotator.Configuration(host=host)
    new_note = utils.change_keys(note, utils.camelcase_to_snakecase)
    with annotator.ApiClient(configuration) as api_client:
        if annotator_type == "date":
            annotations = _annotate_date(api_client, new_note)
        elif annotator_type == "person":
            annotations = _annotate_person(api_client, new_note)
        elif annotator_type == "address":
            annotations = _annotate_address(api_client, new_note)
        else:
            raise ValueError(f"Invalid annotator_type: {annotator_type}")
        sanitized_annotations = api_client.sanitize_for_serialization(
            annotations
        )
    return sanitized_annotations


def get_annotator(host: str) -> Tool:
    """Get annotater service

    Args:
        host: Annotation Service host IP

    Returns:
        Service object

    Examples:
        >>> tool = get_annotator(host="0.0.0.0/api/v1")

    """
    # host = "http://10.23.55.45:9000/api/v1"
    configuration = annotator.Configuration(host=host)
    with annotator.ApiClient(configuration) as api_client:
        tool_instance = tool_api.ToolApi(api_client)
        tool_info = tool_instance.get_tool()
    return tool_info
