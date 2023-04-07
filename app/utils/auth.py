from functools import wraps

import jwt
from flask import request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError

from app.core.exceptions import AppException
from app.enums import TokenTypeEnum
from config import Config


def auth_required():
    def authorize_user(func):
        """
        A wrapper to authorize an action using
        :param func: {function}` the function to wrap around
        :return:
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            authorization_header = request.headers.get("Authorization")
            if not authorization_header or len(authorization_header.split()) < 2:
                raise AppException.Unauthorized("missing authentication token")
            token = authorization_header.split()[1]
            payload = decode_token(token=token)
            if payload.get("token_type") != TokenTypeEnum.access_token.value:
                raise AppException.ValidationException(
                    error_message="token invalid. access token required"
                )
            return func(*args, **kwargs)

        return view_wrapper

    return authorize_user


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            key=Config.SECRET_KEY,
            algorithms=Config.JWT_ALGORITHMS,
        )
        return payload
    except ExpiredSignatureError as e:
        raise AppException.ExpiredTokenException(error_message=e.args)
    except InvalidTokenError as e:
        raise AppException.OperationError(error_message=e.args)
    except PyJWTError as e:
        raise AppException.OperationError(error_message=e.args)
