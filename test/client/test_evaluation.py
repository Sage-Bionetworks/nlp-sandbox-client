"""Test evaluation code"""
import math
import os

from nlpsandboxclient import evaluation, utils

class TestEvaluation:
    """Test evaluation"""

    def setup_method(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.pred_filepath = os.path.join(script_dir,
                                          "../data/new_prediction.json")
        self.gold_filepath = os.path.join(script_dir,
                                          "../data/new_goldstandard.json")

    def test_date(self):
        """Test date evaluation"""
        expected_results = {
            'date_location': [
                {'metric': 'F1', 'value': 0.75, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'precision', 'value': 0.75, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'recall', 'value': 0.75, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'F1', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'precision', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'recall', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'F1', 'value': 0.67, 'type': 'token', 'mode': 'strict'},
                {'metric': 'precision', 'value': 0.6, 'type': 'token', 'mode': 'strict'},
                {'metric': 'recall', 'value': 0.75, 'type': 'token', 'mode': 'strict'}
            ],
            'date_type': [
                {'metric': 'F1', 'value': None},
                {'metric': 'precision', 'value': None},
                {'metric': 'recall', 'value': None}
            ]
        }
        date_evaluator = evaluation.DateEvaluation()
        date_evaluator.convert_dict(self.pred_filepath, self.gold_filepath)
        results = date_evaluator.eval()
        for date_type in results['date_type']:
            if math.isnan(date_type['value']):
                date_type['value'] = None
        assert results == expected_results

    def test_person(self):
        """Test person evaluation"""
        expected_results = {
            'person_location': [
                {'metric': 'F1', 'value': 0.5, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'precision', 'value': 0.5, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'recall', 'value': 0.5, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'F1', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'precision', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'recall', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'F1', 'value': 0.77, 'type': 'token', 'mode': 'strict'},
                {'metric': 'precision', 'value': 0.83, 'type': 'token', 'mode': 'strict'},
                {'metric': 'recall', 'value': 0.71, 'type': 'token', 'mode': 'strict'}
            ],
            'person_type': [
                {'metric': 'F1', 'value': None},
                {'metric': 'precision', 'value': None},
                {'metric': 'recall', 'value': None}
            ]
        }
        evaluator = evaluation.PersonNameEvaluation()
        evaluator.convert_dict(self.pred_filepath, self.gold_filepath)
        results = evaluator.eval()
        for person_type in results['person_type']:
            if math.isnan(person_type['value']):
                person_type['value'] = None
        assert results == expected_results

    def test_address(self):
        """Test person evaluation"""
        expected_results = {
            'address_location': [
                {'metric': 'F1', 'value': 0.75, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'precision', 'value': 0.75, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'recall', 'value': 0.75, 'type': 'instance', 'mode': 'relax'},
                {'metric': 'F1', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'precision', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'recall', 'value': 0.5, 'type': 'instance', 'mode': 'strict'},
                {'metric': 'F1', 'value': 0.67, 'type': 'token', 'mode': 'strict'},
                {'metric': 'precision', 'value': 0.75, 'type': 'token', 'mode': 'strict'},
                {'metric': 'recall', 'value': 0.6, 'type': 'token', 'mode': 'strict'}
            ],
            'address_type': [
                {'metric': 'F1', 'value': 0.5},
                {'metric': 'precision', 'value': 0.5},
                {'metric': 'recall', 'value': 0.5}
            ]
        }
        evaluator = evaluation.PhysicalAddressEvaluation()
        evaluator.convert_dict(self.pred_filepath, self.gold_filepath)
        results = evaluator.eval()
        assert results == expected_results
