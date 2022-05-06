from typing import Union
from .validator import Validator, ValidationError, StopValidation


class Numeric(Validator):
    def __init__(self, message: Union[str, None] = None, parse: bool = True) -> None:
        self.parse = parse
        self.message = message

    def parse_data(self, value: str) -> Union[int, float]:
        try:
            return int(value)
        except ValueError:
            return float(value)

    def handler(self, value, field, request):
        try:
            int(value)
        except ValueError:
            try:
                float(value)
            except ValueError:
                raise ValidationError(self.message)
