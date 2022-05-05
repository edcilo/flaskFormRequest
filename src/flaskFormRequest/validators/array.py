from typing import Union
from .validator import Validator, ValidationError, StopValidation


class Array(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field must an a list or tuple.'

    def handler(self, value, field, request):
        if not isinstance(value, list) and not isinstance(value, tuple):
            raise ValidationError(self.message)
