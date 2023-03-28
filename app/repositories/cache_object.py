import json

from marshmallow import Schema

from app import db
from app.services import RedisService


def cache_object(
    obj_data: db.Model, obj_schema: Schema, cache_key: str, redis_instance: RedisService
):
    """
    This function takes a model object, convert it to string and cache it in redis
    :param obj_data: {Model} object to cache
    :param obj_schema: {Schema} object serializer
    :param cache_key: {str} name of the object
    :param redis_instance: {RedisService} redis server instance
    :return: {Model} object to cache
    """

    serialize_object = obj_schema.dumps(obj_data)
    redis_instance.set(cache_key, serialize_object)

    return obj_data


def cache_list_of_object(
    obj_data: db.Model, obj_schema: Schema, cache_key: str, redis_instance: RedisService
):
    """
    This function takes a list of model object, convert it to string and cache it in
    redis
    :param obj_data: {list} list of object to cache
    :param obj_schema: {Schema} object serializer
    :param cache_key: {str} name of the object
    :param redis_instance: {RedisService} redis server instance
    :return: {Model} object to cache
    """

    serialize_all_object = obj_schema.dumps(obj_data, many=True)
    redis_instance.set(cache_key, serialize_all_object)

    return obj_data


def deserialize_cached_object(obj_data: str, obj_model: db.Model, obj_schema: Schema):
    """
    This function takes a cache object, typecast it to a model object
    :param obj_data: {str} object to deserialize
    :param obj_model: {Model} object model to typecast to
    :param obj_schema: {Schema} object serializer
    :return: {Model} deserialized object
    """

    deserialized_object = obj_schema.loads(json.dumps(obj_data))

    return obj_model(**deserialized_object)


def deserialize_list_of_cached_object(
    obj_data: list, obj_model: db.Model, obj_schema: Schema
):
    """
    This function takes a list of cache object, typecast it the objects to a model object
    :param obj_data: {list} object to deserialize
    :param obj_model: {Model} object model to typecast
    :param obj_schema: {Schema} object serializer
    :return: {list} deserialized object
    """

    deserialize_objects = obj_schema.loads(json.dumps(obj_data), many=True)
    for count, value in enumerate(deserialize_objects):
        deserialize_objects[count] = obj_model(**value)

    return deserialize_objects
