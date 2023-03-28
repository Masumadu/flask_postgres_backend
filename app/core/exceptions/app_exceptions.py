from typing import Union

from flask import Response, current_app, json
from sqlalchemy.exc import DBAPIError
from werkzeug.exceptions import HTTPException


class AppExceptionCase(Exception):
    def __init__(
        self,
        status_code: int,
        error_message: Union[any, None],
        context: Union[any],
    ):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.error_message = error_message
        self.context = context
        if self.context:
            current_app.logger.critical(self.context)
        else:
            if self.error_message:
                current_app.logger.error(self.error_message)

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code = {self.status_code} - error_message = {self.error_message}"
        )


def app_exception_handler(exc):
    if isinstance(exc, DBAPIError):
        return Response(
            json.dumps(
                {"app_exception": "Database Error", "errorMessage": exc.orig.pgerror}
            ),
            status=400,
        )
    if isinstance(exc, HTTPException):
        return Response(
            json.dumps({"app_exception": "HTTP Error", "errorMessage": exc.description}),
            status=exc.code,
        )
    return Response(
        json.dumps(
            {"app_exception": exc.exception_case, "errorMessage": exc.error_message}
        ),
        status=exc.status_code,
        mimetype="application/json",
    )


class AppException:
    class OperationError(AppExceptionCase):
        """
        Generic Exception to catch failed operations
        """

        def __init__(self, error_message: Union[any, None], context: Union[any] = None):
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context)

    class InternalServerError(AppExceptionCase):
        """
        Generic Exception to catch failed operations
        """

        def __init__(self, error_message: Union[any, None], context: Union[any] = None):
            status_code = 500
            AppExceptionCase.__init__(self, status_code, error_message, context)

    class ResourceExists(AppExceptionCase):
        """
        Resource Creation Failed Exception
        """

        def __init__(self, error_message: Union[any, None], context: Union[any] = None):
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context)

    class NotFoundException(AppExceptionCase):
        def __init__(self, error_message: Union[any, None], context: Union[any] = None):
            """
            Resource does not exist
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, error_message, context)

    class Unauthorized(AppExceptionCase):
        def __init__(self, error_message: Union[any, None], context: Union[any] = None):
            """
            Unauthorized
            :param context: extra dictionary object to give the error more context
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, error_message, context)

    class ValidationException(AppExceptionCase):
        """
        Resource Creation Failed Exception
        """

        def __init__(self, error_message: Union[any, None], context: Union[any] = None):
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context)

    class BadRequest(AppExceptionCase):
        def __init__(self, error_message: Union[any, None], context: Union[any] = None):
            """
            Bad Request

            :param context:
            """
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context)

    class ExpiredTokenException(AppExceptionCase):
        def __init__(self, error_message: Union[any, None], context: [Union] = None):
            """
            Expired Token
            :param context:
            """

            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context)
