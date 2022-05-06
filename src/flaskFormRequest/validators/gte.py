from typing import Union
from collections.abc import Iterable
from .validator import Validator, ValidationError, StopValidation


class Gte(Validator):
    def __init__(self, length: int, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.size = length
        self.message = message or 'This field is not valid.'

    def handler(self, value, field, request):
        hasError = False
        # TODO: implement support for files
        if isinstance(value, int) or isinstance(value, float):
            hasError = value < self.size
        else:
            hasError = len(value) < self.size
        
        if hasError:
            raise ValidationError(self.message)
