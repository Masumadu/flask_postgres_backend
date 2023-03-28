import json

import redis
from redis.exceptions import RedisError

from app.core.exceptions import HTTPException
from app.core.service_interfaces import CacheServiceInterface
from config import Config

REDIS_SERVER = Config.REDIS_SERVER
REDIS_PASSWORD = Config.REDIS_PASSWORD
REDIS_PORT = Config.REDIS_PORT

redis_conn = redis.Redis(
    host=REDIS_SERVER, port=REDIS_PORT, db=0, password=REDIS_PASSWORD
)


class RedisService(CacheServiceInterface):
    def set(self, name, data):
        """

        :param name: {string} name of the object you want to set
        :param data: {Any} the object you want to set
        :return: {None}
        """
        try:
            redis_conn.set(name, data)
            return True
        except RedisError:
            raise HTTPException(status_code=500, description="Error adding to cache")

    def get(self, name):
        """

        :param name: {string} name of the object you want to get
        :return: {Any}
        """
        try:
            data = redis_conn.get(name)
            if data:
                return json.loads(data)
            return data
        except RedisError:
            raise HTTPException(status_code=500, description="Error getting from cache")

    def delete(self, name):
        """
        :param name: {string} name of the object you want to delete
        :return: {Bool}
        """
        try:
            redis_conn.delete(name)
        except RedisError:
            raise HTTPException(status_code=500, description="Error deleting from cache")
