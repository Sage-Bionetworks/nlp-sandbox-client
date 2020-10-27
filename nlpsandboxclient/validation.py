"""Validation of data and platform components like NLP Tools"""

from jsonschema import Draft7Validator

from .client import NlpClient


class NlpToolClient(NlpClient):
    """Client for developed Nlp Tools"""
    def __init__(self, tool_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool_type = tool_type

    def validate(self):
        """Validate schema"""
        # Check schema is correct first
        Draft7Validator.check_schema(schema)
        schema_validator = Draft7Validator(schema)
        # Create error message to location mapping
        error_map = {}
        for error in schema_validator.iter_errors(data):
            if error_map.get(error.message) is None:
                error_map[error.message] = [_parse_path(error.absolute_path)]
            else:
                error_map[error.message].append(_parse_path(error.absolute_path))
        final_error_list = []
        for error in error_map:
            # If the json is completely incorrect, it will have error list ['']
            if error_map[error] == ['']:
                error_string = f'{error}\n'
            else:
                errors = "\n  ".join(error_map[error])
                error_string = f'{error} at\n  {errors}\n'
            final_error_list.append(error_string)
        return final_error_list
