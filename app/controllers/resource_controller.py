import uuid

from app.core import Result
from app.core.exceptions import AppException
from app.core.notifications.notifier import Notifier
from app.repositories import ResourceRepository
from app.services import AuthService

ASSERT_OBJECT_DATA = "missing object data"
ASSERT_OBJECT_ID = "missing object id"
ASSERT_OBJECT_IS_DICT = "object not a dict"
OBJECT_NOT_FOUND = "object does not exist"


class ResourceController(Notifier):
    def __init__(
        self, resource_repository: ResourceRepository, auth_service: AuthService
    ):
        self.resource_repository = resource_repository
        self.auth_service = auth_service

    def create_resource(self, obj_data: dict):
        assert obj_data, ASSERT_OBJECT_IS_DICT

        result = self.resource_repository.create(obj_data)

        return Result(result, 201)

    def get_all_resources(self, query_param: dict):
        result = self.resource_repository.paginate(
            page=int(query_param.get("page", 1)),
            per_page=int(query_param.get("per_page", 10)),
        )
        return Result(result, 200)

    def get_resource(self, obj_id: str):
        assert obj_id, ASSERT_OBJECT_ID

        try:
            result = self.resource_repository.get_by_id(obj_id)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(error_message=OBJECT_NOT_FOUND)

        return Result(result, 200)

    def update_resource(self, obj_id: str, obj_in: dict):
        assert obj_in, ASSERT_OBJECT_IS_DICT
        assert obj_id, ASSERT_OBJECT_ID

        try:
            result = self.resource_repository.update_by_id(obj_id=obj_id, obj_in=obj_in)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(error_message=OBJECT_NOT_FOUND)

        return Result(result, 200)

    def delete_resource(self, obj_id: str):
        assert obj_id, ASSERT_OBJECT_ID

        try:
            self.resource_repository.delete_by_id(obj_id)
        except AppException.NotFoundException:
            raise AppException.NotFoundException(error_message=OBJECT_NOT_FOUND)

        return Result(None, 204)

    def get_token(self):
        token = self.auth_service.get_token(user_id=str(uuid.uuid4()))

        return Result(token, 200)

    def get_refresh_token(self, query_params: dict):
        assert query_params, ASSERT_OBJECT_IS_DICT

        refresh_token = query_params.get("refresh_token")
        token = self.auth_service.refresh_token(refresh_token=refresh_token)

        return Result(token, 200)
