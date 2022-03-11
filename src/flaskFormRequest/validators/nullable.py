from typing import Union
from werkzeug.datastructures import FileStorage
from .validator import Validator, NoneValueException


class Nullable(Validator):
    def handler(self, value, field, request):
        if value is None or (isinstance(value, FileStorage) and value.content_type is None):
            raise NoneValueException(self.message)
