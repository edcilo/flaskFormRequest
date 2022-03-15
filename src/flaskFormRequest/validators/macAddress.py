import re
from typing import Union
from .validator import Validator, ValidationError, StopValidation


class MacAddress(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'The field must be a valid MAC address'

    def handler(self, value, field, request):
        if not re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
            raise ValidationError(self.message)
