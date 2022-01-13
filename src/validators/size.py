from typing import Union
from .validator import Validator, ValidationError


class Size(Validator):
    def __init__(self, length: int, message: Union[str, None] = None) -> None:
        self.size = length
        self.message = message or 'The :attribute must be :size characters.'

    def __call__(self, request, value):
        if len(value) != self.size:
            raise ValidationError(self.message)
        return value
