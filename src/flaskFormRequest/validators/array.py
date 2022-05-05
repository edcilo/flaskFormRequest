import json
from typing import Union
from .validator import (
    CollectionErrors, 
    NoneValueException, 
    Validator, 
    ValidationError, 
    StopValidation
)


class Array(Validator):
    def __init__(self, 
                 message: Union[str, None] = None, 
                 parse: bool = True, 
                 rules: Union[list, tuple, None] = None) -> None:
        self.parse = parse
        self.message = message or 'This field must be a list or tuple.'
        self.rules = rules

    def handler(self, value, field, request):
        if not isinstance(value, list):
            raise ValidationError(self.message)
        errors = self.array_handler(value, field, request)
        if len(errors) > 0:
            raise CollectionErrors(errors)

    def array_handler(self, value, field, request):
        allErrors = dict()
        if self.rules is not None:
            for i in range(len(value)):
                fieldname = f"{field}.{i}"
                errors = []
                for validator in self.rules:
                    try:
                        value[i] = validator(value[i], fieldname, field, request)
                    except StopValidation as err:
                        errors.append(str(err))
                        break
                    except ValidationError as err:
                        errors.append(str(err))
                    except CollectionErrors as err:
                        errors.append(err.errors)
                    except NoneValueException:
                        break
                if len(errors) > 0:
                    allErrors[fieldname] = errors
        return allErrors
