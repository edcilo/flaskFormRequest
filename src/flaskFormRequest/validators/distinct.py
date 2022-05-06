from typing import Any, Union
from .validator import Validator, ValidationError, StopValidation


class Distinct(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field is not valid.'

    def handler(self, value, field, request):
        if len(value) != len(set(value)):
            raise ValidationError(self.message)
