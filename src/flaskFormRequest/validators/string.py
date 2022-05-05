from typing import Union
from .validator import Validator, ValidationError, StopValidation


class String(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field must be an integer.'

    def parse_data(self, value):
        return str(value)

    def handler(self, value, field, request):
        try:
            value = str(value)
        except:
            raise StopValidation(self.message)
