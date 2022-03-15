import json
from typing import Union
from .validator import Validator, ValidationError, StopValidation


class Json(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field must be a valid JSON string.'

    def parse_data(self, value):
        return json.loads(value)

    def handler(self, value, field, request):
        try:
            json.loads(value)
        except ValueError:
            raise ValidationError(self.message)

