import abc
from typing import Any


class ValidationError(ValueError):
    def __init__(self, message="", *args, **kwargs):
        ValueError.__init__(self, message, *args, **kwargs)


class StopValidation(Exception):
    def __init__(self, message="", *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)


class Validator(abc.ABC):
    message = 'This field is invalid'

    def parse_data(self, value: Any) -> Any:
        return value

    @abc.abstractmethod
    def __call__(self, request, value):
        pass
