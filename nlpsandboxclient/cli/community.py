#!/usr/bin/env python3
import click

from nlpsandboxclient import utils


# Command Group
@click.group(name='community', no_args_is_help=True)
def cli():
    """Commands for NLP Sandbox users."""


@cli.command()
def get_num_users():
    """Gets the number of NLP Sandbox users"""
    syn = utils.synapse_login()
    res = syn.restGET("/teamMembers/count/3413388")
    print(f"Number of NLP sandbox users: {res['count']}")


if __name__ == '__main__':
    cli()
