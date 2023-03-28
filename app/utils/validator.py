from functools import wraps

from flask import request

from app.core.exceptions import AppException


def validator(schema):
    def validate_data(func):
        """
        A wrapper to validate data using marshmallow schema
        :param func: {function} the function to wrap around
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            errors = schema().validate(request.json)
            if errors:
                raise AppException.ValidationException(error_message=errors)

            return func(*args, **kwargs)

        return view_wrapper

    return validate_data


def arg_validator(schema, param):
    def validate_args(func):
        """
        A wrapper to validate uuid using marshmallow schema
        :param func: {function} the function to wrap around
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            if request.view_args:
                request_parameters: dict = request.view_args
            else:
                request_parameters: dict = request.args
            errors = schema().validate(
                {arg: request_parameters.get(arg) for arg in param.split("|")}
            )
            if errors:
                raise AppException.ValidationException(error_message=errors)

            return func(*args, **kwargs)

        return view_wrapper

    return validate_args
