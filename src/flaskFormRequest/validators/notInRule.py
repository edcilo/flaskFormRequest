from typing import Union
from .validator import Validator, ValidationError, StopValidation


class NotIn(Validator):
    def __init__(self, no_accepted_values = Union[list, tuple], message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field is not valid.'
        self.no_accepted_values = no_accepted_values

    def handler(self, value, field, request):
        if value in self.no_accepted_values:
            raise ValidationError(self.message)
