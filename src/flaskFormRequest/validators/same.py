from typing import Any, Union
from .validator import Validator, ValidationError, StopValidation


class Same(Validator):
    def __init__(self, match: Any, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.match = match
        self.message = message or 'This field is not valid.'

    def handler(self, value, field, request):
        if value != self.match:
            raise ValidationError(self.message)
