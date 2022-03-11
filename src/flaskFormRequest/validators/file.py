from typing import Union
from werkzeug.datastructures import FileStorage
from .validator import Validator, ValidationError, StopValidation


class File(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field must be a file'

    def handler(self, value, field, request):
        if not isinstance(value, FileStorage):
            raise ValidationError(self.message)

