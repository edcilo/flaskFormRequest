from .validator import Validator, ValidationError, StopValidation


class Required(Validator):
    message = 'This field is required'

    def __call__(self, request, value):
        if value is None or len(value) == 0:
            raise StopValidation(self.message)
        return value
