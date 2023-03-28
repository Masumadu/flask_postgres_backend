from app.core.exceptions import HTTPException
from app.core.repository import SQLBaseRepository
from app.models import ResourceModel
from app.schema import ResourceSchema
from app.services import RedisService

from .cache_object import (
    cache_list_of_object,
    cache_object,
    deserialize_cached_object,
    deserialize_list_of_cached_object,
)

SINGLE_RESOURCE_CACHE_KEY = "resource_{}"
ALL_RESOURCES_CACHE_KEY = "all_resources"


class ResourceRepository(SQLBaseRepository):

    model = ResourceModel

    def __init__(self, redis_service: RedisService, resource_schema: ResourceSchema):
        self.redis_service = redis_service
        self.resource_schema = resource_schema
        super().__init__()

    def index(self):
        try:
            redis_data = self.redis_service.get(ALL_RESOURCES_CACHE_KEY)
            if redis_data:
                deserialized_objects = deserialize_list_of_cached_object(
                    obj_data=redis_data,
                    obj_schema=self.resource_schema,
                    obj_model=self.model,
                )
                return deserialized_objects
            postgres_data = cache_list_of_object(
                obj_data=super().index(),
                obj_schema=self.resource_schema,
                redis_instance=self.redis_service,
                cache_key=ALL_RESOURCES_CACHE_KEY,
            )
            return postgres_data
        except HTTPException:
            return super().index()

    def create(self, obj_data: dict):
        postgres_data = super().create(obj_data)
        try:
            obj_data = cache_object(
                obj_data=postgres_data,
                obj_schema=self.resource_schema,
                redis_instance=self.redis_service,
                cache_key=SINGLE_RESOURCE_CACHE_KEY.format(postgres_data.id),
            )
            _ = cache_list_of_object(
                obj_data=super().index(),
                obj_schema=self.resource_schema,
                redis_instance=self.redis_service,
                cache_key=ALL_RESOURCES_CACHE_KEY,
            )
            return obj_data
        except HTTPException:
            return postgres_data

    def get_by_id(self, obj_id: str):
        try:
            redis_data = self.redis_service.get(
                SINGLE_RESOURCE_CACHE_KEY.format(obj_id)
            )
            if redis_data:
                deserialized_object = deserialize_cached_object(
                    obj_data=redis_data,
                    obj_model=self.model,
                    obj_schema=self.resource_schema,
                )
                return deserialized_object
            object_data = cache_object(
                obj_data=super().find_by_id(obj_id),
                obj_schema=self.resource_schema,
                redis_instance=self.redis_service,
                cache_key=SINGLE_RESOURCE_CACHE_KEY.format(obj_id),
            )
            return object_data
        except HTTPException:
            return super().find_by_id(obj_id)

    def update_by_id(self, obj_id: str, obj_in: dict):
        postgres_data = super().update_by_id(obj_id, obj_in)
        try:
            redis_data = self.redis_service.get(
                SINGLE_RESOURCE_CACHE_KEY.format(obj_id)
            )
            if redis_data:
                self.redis_service.delete(SINGLE_RESOURCE_CACHE_KEY.format(obj_id))
            object_data = cache_object(
                obj_data=postgres_data,
                obj_schema=self.resource_schema,
                redis_instance=self.redis_service,
                cache_key=SINGLE_RESOURCE_CACHE_KEY.format(postgres_data.id),
            )
            _ = cache_list_of_object(
                obj_data=super().index(),
                obj_schema=self.resource_schema,
                redis_instance=self.redis_service,
                cache_key=ALL_RESOURCES_CACHE_KEY,
            )
            return object_data
        except HTTPException:
            return super().update_by_id(obj_id, obj_in)

    def delete_by_id(self, obj_id):
        postgres_data = super().delete_by_id(obj_id)
        try:
            redis_data = self.redis_service.get(
                SINGLE_RESOURCE_CACHE_KEY.format(obj_id)
            )
            if redis_data:
                self.redis_service.delete(SINGLE_RESOURCE_CACHE_KEY.format(obj_id))
            _ = cache_list_of_object(
                obj_data=super().index(),
                obj_schema=self.resource_schema,
                redis_instance=self.redis_service,
                cache_key=ALL_RESOURCES_CACHE_KEY,
            )
            return postgres_data
        except HTTPException:
            return super().delete_by_id(obj_id)
