import socket
from typing import Union
from .validator import Validator, ValidationError, StopValidation


class IP(Validator):
    def __init__(self, version: str = 'v4', message: Union[str, None] = None, parse: bool = True) -> None:
        self.version = version
        self.parse = parse
        self.message = message or 'The attribute must be a valid IP address.'

    def handler(self, value, field, request):
        if self.version not in ('v4', 'v6'):
            raise ValidationError("The param version is invalid, use v4 or v6")

        try:
            if self.version == 'v4':
                socket.inet_aton(value)
            elif self.version == 'v6':
                socket.inet_pton(socket.AF_INET6, value)
        except socket.error:
            raise ValidationError(self.message)
