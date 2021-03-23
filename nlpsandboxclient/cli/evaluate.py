#!/usr/bin/env python3
import click

from nlpsandboxclient import evaluation, utils


@click.group(name='evaluate', no_args_is_help=True)
def cli():
    """Evaluation related commands"""


@cli.command(name="evaluate-prediction", no_args_is_help=True)
@click.option('--pred_filepath', help='Prediction filepath',
              type=click.Path(exists=True), required=True)
@click.option('--gold_filepath', help='Gold standard filepath',
              type=click.Path(exists=True), required=True)
@click.option('--output', help='Specify output json path',
              type=click.Path())
@click.option('--tool_type', help='The type of tool to evaluate.',
              type=click.Choice(['nlpsandbox:date-annotator',
                                 'nlpsandbox:person-name-annotator',
                                 'nlpsandbox:physical-address-annotator'],
                                case_sensitive=False), required=True)
def evaluate_prediction(pred_filepath, gold_filepath, output, tool_type):
    """Evaluate the performance of a prediction file. Example prediction and
    goldstandard files are found in test/data/new_prediction.json and
    test/data/new_goldstandard.json respectively.
    """
    eval_mapping = {
        "nlpsandbox:date-annotator": evaluation.DateEvaluation,
        "nlpsandbox:person-name-annotator": evaluation.PersonNameEvaluation,
        "nlpsandbox:physical-address-annotator": evaluation.PhysicalAddressEvaluation
    }
    evaluator = eval_mapping[tool_type]()

    evaluator.convert_dict(pred_filepath, gold_filepath)
    results = evaluator.eval()
    utils.stdout_or_json(results, output)


if __name__ == '__main__':
    cli()
