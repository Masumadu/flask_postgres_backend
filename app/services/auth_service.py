from dataclasses import dataclass
from config import Config
from app.core.exceptions import AppException
from app.core.service_interfaces import AuthServiceInterface
import jwt
from datetime import datetime, timedelta
from app.utils.auth import decode_token
from app.enums import TokenTypeEnum

REFRESH_TOKEN_EXPIRATION = Config.ACCESS_TOKEN_EXPIRATION + timedelta(minutes=30)


@dataclass
class AuthService(AuthServiceInterface):

    def get_token(self, user_id: str):
        access_token = self.generate_token(
            user_id=user_id,
            token_type=TokenTypeEnum.access_token.value,
            expiration=Config.ACCESS_TOKEN_EXPIRATION
        )
        refresh_token = self.generate_token(
            user_id=user_id,
            token_type=TokenTypeEnum.refresh_token.value,
            expiration=REFRESH_TOKEN_EXPIRATION
        )

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_token(self, refresh_token: str):
        token = decode_token(token=refresh_token)
        if token.get("token_type") != TokenTypeEnum.refresh_token.value:
            raise AppException.OperationError(error_message="token invalid")
        token = self.get_token(token.get("user_id"))

        return token

    # noinspection PyMethodMayBeStatic
    def generate_token(self, user_id: str, token_type: str, expiration: datetime):
        payload = {
            "id": user_id,
            "token_type": token_type,
            "exp": expiration
        }
        token = jwt.encode(
            payload=payload, key=Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHMS
        )
        return token

    def create_user(self, obj_data: dict):
        assert obj_data, "Missing request data to be saved"
        assert isinstance(obj_data, dict)
        # TODO: create user in authentication server
        return obj_data

    def update_user(self, obj_in: dict):
        assert obj_in, "Missing request data to update with"
        assert isinstance(obj_in, dict), "request data is not a dict"
        # TODO: update user in authentication server
        return obj_in

    def reset_password(self, obj_in: dict):
        assert obj_in, "Missing request data to update with"
        assert isinstance(obj_in, dict), "request data is not a dict"
        # TODO: reset user password in authentication server
        return obj_in

    def delete_user(self, user_id: str):
        assert user_id, "Missing id of object to be deleted"
        assert isinstance(user_id, str)
        # TODO: delete user in authentication server
        return True
