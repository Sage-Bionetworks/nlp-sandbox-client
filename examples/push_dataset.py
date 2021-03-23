"""
Example code to push a dataset into the data node. A complete
dataset includes "Dataset", "Fhir Store", "Annotation Store",
"Annotation", "Patient", "Note"

To run this code, here are the requirements:

- Install the nlpsandbox-client (`pip install nlpsandbox-client`)
- Start the Data Node locally - Follow instructions here:
https://github.com/nlpsandbox/data-node
- python push_dataset.py

"""
import json

import datanode
import datanode.apis
import datanode.models
from datanode.rest import ApiException
import nlpsandboxclient.utils


# Defining the host is optional and defaults to http://example.com/api/v1
# See configuration.py for a list of all supported configuration parameters.
host = "http://localhost:8080/api/v1"
configuration = datanode.Configuration(host=host)

dataset_id = 'test-dataset'
fhir_store_id = 'evaluation'
annotation_store_id = 'goldstandard'
json_filename = "example-patient-bundles.json"


with datanode.ApiClient(configuration) as api_client:
    dataset_api = datanode.apis.DatasetApi(api_client)
    fhir_store_api = datanode.apis.FhirStoreApi(api_client)
    annotation_store_api = datanode.apis.AnnotationStoreApi(api_client)
    patient_api = datanode.apis.PatientApi(api_client)
    note_api = datanode.apis.NoteApi(api_client)
    annotation_api = datanode.apis.AnnotationApi(api_client)

    # The example is always deleted
    try:
        # get the dataset
        dataset = dataset_api.get_dataset(dataset_id)
        # delete the dataset
        print(f"Deleting exist dataset: {dataset_id}")
        dataset_api.delete_dataset(dataset_id)
    except ApiException:
        pass

    # create dataset if not found
    print(f"Creating dataset: {dataset_id}")
    dataset = dataset_api.create_dataset(
        dataset_id,
        body={}
    )

    print(f"Creating Fhir Store: {fhir_store_id}")
    fhir_store = fhir_store_api.create_fhir_store(
        dataset_id, fhir_store_id,
        body={}
    )

    print(f"Creating Annotation Store: {annotation_store_id}")
    annotation_store = annotation_store_api.create_annotation_store(
        dataset_id, annotation_store_id,
        body={}
    )

    with open(json_filename) as f:
        data = json.load(f)
        patient_bundles = data['patient_bundles']

    for patient_bundle in patient_bundles:
        # Create or get a FHIR Patient
        patient = nlpsandboxclient.utils.change_keys(
            patient_bundle['patient'],
            nlpsandboxclient.utils.camelcase_to_snakecase
        )
        patient_id = patient.pop("identifier")
        print(f"Creating patient: {patient_id}")
        patient_api.create_patient(
            dataset_id, fhir_store_id, patient_id,
            patient_create_request=patient
        )

        # Create the Note and Annotation objects linked to the patient
        note_bundles = patient_bundle['note_bundles']

        for note_bundle in note_bundles:
            # Determine note Id since noteId isn't part of the 'note'
            annotation = note_bundle['annotation']
            annotations_cols = ['textDateAnnotations',
                                'textPhysicalAddressAnnotations',
                                'textPersonNameAnnotations']
            note_ids = set()
            for col in annotations_cols:
                for annot in annotation[col]:
                    note_ids.add(annot['noteId'])
            assert len(note_ids) == 1, "Must only have one noteId"
            note_id = list(note_ids)[0]

            # Create Note
            note = nlpsandboxclient.utils.change_keys(
                note_bundle['note'],
                nlpsandboxclient.utils.camelcase_to_snakecase
            )
            note['patient_id'] = patient_id

            print(f"Creating note ({note_id}) for patient ({patient_id})")
            note_api.create_note(
                dataset_id, fhir_store_id, note_id,
                note_create_request=note
            )
            # Create annotation
            annotation['annotationSource']['resourceSource']['name'] = \
                "{fhir_store_name}/fhir/Note/{note_id}".format(
                    fhir_store_name=fhir_store.name,
                    note_id=note_id
                )
            new_annotation = nlpsandboxclient.utils.change_keys(
                annotation,
                nlpsandboxclient.utils.camelcase_to_snakecase
            )
            print(f"Creating annotation for note: {note_id}")
            annotation = annotation_api.create_annotation(
                dataset_id, annotation_store_id,
                annotation_id=note_id,
                annotation_create_request=new_annotation
            )
