from typing import Callable, Union
from .validator import Validator, ValidationError, StopValidation


class Callable(Validator):
    def __init__(self, check_function: Callable, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message or 'This field is not valid'
        self.check_function = check_function

    def handler(self, value, field, request):
        if not self.check_function(value, field, request):
            raise ValidationError(self.message)
