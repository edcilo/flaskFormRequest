import functools
from flask import jsonify, request


def form_validator(FormClass):
    def form_validator_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            form = FormClass(request)
            if not form.validate():
                return jsonify({'errors': form.errors}), 400
            kwargs['form'] = form
            return func(*args, **kwargs)
        return wrapper
    return form_validator_decorator
