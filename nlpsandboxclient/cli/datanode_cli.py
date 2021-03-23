"""Data node CLI"""
import json

import click

from nlpsandboxclient import client, utils
from nlpsandboxclient.client import DATA_NODE_HOST


# Command Group
@click.group(name='datanode', no_args_is_help=True)
def cli():
    """Commands to interact with NLP Data Node."""


@cli.command(no_args_is_help=True)
@click.option('--output', help='Output json filepath', type=click.Path())
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--dataset_id', help='Dataset id', required=True)
@click.option('--fhir_store_id', help='Dataset id', required=True)
def list_notes(output, data_node_host, dataset_id, fhir_store_id):
    """Gets clinical notes of a NLP data node FHIR store."""
    clinical_notes = client.list_notes(host=data_node_host,
                                       dataset_id=dataset_id,
                                       fhir_store_id=fhir_store_id)
    # Stdout or store to json
    utils.stdout_or_json(list(clinical_notes), output)


@cli.command(no_args_is_help=True)
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--dataset_id', help='Dataset id')
@click.option('--annotation_store_id', help='Annotation store id',
              required=True)
@click.option('--annotation_json', help='Json file with annotations to store',
              type=click.Path(exists=True), required=True)
def store_annotations(data_node_host, dataset_id, annotation_store_id,
                      annotation_json):
    """Store annotations in an NLP data node annotation store.
    The annotation store is deleted if it already exists.
    Sets the annotation_id as the note id.
    """
    with open(annotation_json, "r") as annot_f:
        annotations = json.load(annot_f)
    # If only one annotation is passed in, turn it into a list
    if isinstance(annotations, dict):
        annotations = [annotations]
    client.store_annotations(
        host=data_node_host,
        dataset_id=dataset_id,
        annotation_store_id=annotation_store_id,
        annotations=annotations
    )


@cli.command(no_args_is_help=True)
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--dataset_id', help='Dataset id', required=True)
@click.option('--annotation_store_id', help='Dataset id', required=True)
@click.option('--create_if_missing', help='Create resource if missing', is_flag=True)
def get_annotation_store(data_node_host, dataset_id, annotation_store_id, create_if_missing):
    """Create annotation store for a NLP data node dataset."""
    # Create annotation store object
    annotation_store = client.get_annotation_store(
        host=data_node_host, dataset_id=dataset_id,
        annotation_store_id=annotation_store_id,
        create_if_missing=create_if_missing
    )
    print(annotation_store.name)


@cli.command(no_args_is_help=True)
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--dataset_id', help='Dataset Id', required=True)
@click.option('--annotation_store_id', help='Dataset Id', required=True)
@click.option('--annotation_id', help='Annotation Id', required=True)
@click.option('--output', help='Output json filepath', type=click.Path())
def get_annotation(data_node_host, dataset_id, annotation_store_id,
                   annotation_id, output):
    """Get annotation for a NLP data node dataset."""
    annotation = client.get_annotation(
        host=data_node_host, dataset_id=dataset_id,
        annotation_store_id=annotation_store_id,
        annotation_id=annotation_id
    )
    utils.stdout_or_json(annotation.to_dict(), output)


@cli.command(no_args_is_help=True)
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--dataset_id', help='Dataset id', required=True)
@click.option('--annotation_store_id', help='Dataset id', required=True)
@click.option('--output', help='Output json filepath', type=click.Path())
def list_annotations(data_node_host, dataset_id, annotation_store_id, output):
    """List annotations of a NLP data node annotation store."""
    # Create annotation store object
    annotations = client.list_annotations(
        host=data_node_host, dataset_id=dataset_id,
        annotation_store_id=annotation_store_id
    )
    utils.stdout_or_json(list(annotations), output)


@cli.command()
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--output', help='Output json filepath', type=click.Path())
def list_datasets(data_node_host, output):
    """List annotations of a NLP data node annotation store."""
    # Create annotation store object
    datasets = client.list_datasets(
        host=data_node_host
    )
    utils.stdout_or_json(list(datasets), output)


@cli.command(no_args_is_help=True)
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--dataset_id', help='Dataset id', required=True)
@click.option('--output', help='Output json filepath', type=click.Path())
def store_dataset(data_node_host, dataset_id, output):
    """Create a dataset in the data node"""
    # Create dataset
    dataset = client.store_dataset(host=data_node_host,
                                   dataset_id=dataset_id)
    utils.stdout_or_json(dataset.to_dict(), output)


@cli.command(no_args_is_help=True)
@click.option('--data_node_host', help='Data node host',
              default=DATA_NODE_HOST, show_default=True)
@click.option('--dataset_id', help='Dataset id', required=True)
def delete_dataset(data_node_host, dataset_id):
    """Delete a dataset in the data node"""
    # Create dataset
    client.delete_dataset(host=data_node_host,
                          dataset_id=dataset_id)

# @cli.command()
# @click.argument('noteid', type=click.INT)
# @click.option('--output', help='Output json filepath', type=click.Path())
# @click.option('--data_node_host',
#               help='Data node host.  If not specified, uses '
#                    'http://0.0.0.0:8080/api/v1')
# def get_clinical_note(noteid, output, data_node_host):
#     """Gets clinical note of NOTEID"""
#     data_node_host = (data_node_host if data_node_host is not None
#                       else client.DATA_NODE_HOST)
#     nlp = DataNodeClient(host=data_node_host)
#     clinical_note = nlp.get_clinical_note(noteid)
#     utils.stdout_or_json(clinical_note, output)


# @cli.command()
# @click.option('--data_node_host',
#               help='Data node host.  If not specified, uses '
#                    'http://0.0.0.0:8080/api/v1')
# def get_health(data_node_host):
#     """Gets health of the API"""
#     data_node_host = (data_node_host if data_node_host is not None
#                       else client.DATA_NODE_HOST)
#     nlp = DataNodeClient(host=data_node_host)
#     print(nlp.get_health())


# @cli.command()
# @click.option('--output', help='Output json filepath', type=click.Path())
# @click.option('--data_node_host',
#               help='Data node host.  If not specified, uses '
#                    'http://0.0.0.0:8080/api/v1')
# def get_dates(output, data_node_host):
#     """Get all date annotations"""
#     data_node_host = (data_node_host if data_node_host is not None
#                       else client.DATA_NODE_HOST)
#     nlp = DataNodeClient(host=data_node_host)
#     dates = nlp.get_dates()
#     utils.stdout_or_json(dates, output)
