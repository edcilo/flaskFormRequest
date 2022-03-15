from typing import Union
from werkzeug.datastructures import FileStorage
from .validator import Validator, ValidationError, StopValidation


class MimeTypes(Validator):
    def __init__(self, types: Union[list, tuple], message: Union[str, None] = None, parse: bool = True) -> None:
        self.types = types
        self.parse = parse
        self.message = message or 'This field is not valid'

    def handler(self, value, field, request):
        if value.mimetype not in self.types:
            raise ValidationError(self.message)
