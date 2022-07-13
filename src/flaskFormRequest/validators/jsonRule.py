import json
from typing import Union
from .validator import (
    CollectionErrors,
    NoneValueException,
    Validator,
    ValidationError,
    StopValidation)


class Json(Validator):
    def __init__(self,
                 message: Union[str, None] = None,
                 parse: bool = True,
                 rules: Union[list, tuple, None] = None) -> None:
        self.parse = parse
        self.message = message or 'This field must be a valid JSON string.'
        self.rules = rules

    def parse_data(self, value):
        return value if isinstance(value, dict) else json.loads(value)

    def handler(self, value, field, request):
        try:
            value = value if isinstance(value, dict) else json.loads(str(value))
            errors = self.json_handler(value, field, request)
            if len(errors) > 0:
                raise CollectionErrors(errors)
        except (ValueError):
            raise ValidationError(self.message)

    def json_handler(self, value, field, request):
        allErrors = dict()
        if self.rules is not None:
            for field, validators in self.rules.items():
                errors = []
                for validator in validators:
                    try:
                        value[field] = validator(value.get(field), field, value, request)
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
                    allErrors[field] = errors
        return allErrors
