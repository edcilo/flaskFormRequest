from collections.abc import Iterable
from typing import Union
from .validator import Validator, ValidationError, StopValidation


class Filled(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field must have a value.'

    def handler(self, value, field, request):
        if value is None \
            or (
                (isinstance(value, str) or isinstance(value, Iterable)) \
                and len(value) == 0
            ):
            raise StopValidation(self.message)
