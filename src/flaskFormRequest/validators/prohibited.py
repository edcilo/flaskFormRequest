from typing import Union
from .validator import Validator, ValidationError, StopValidation


class Prohibited(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field is required'

    def handler(self, value, field, request):
        if bool(value):
            raise StopValidation(self.message)
