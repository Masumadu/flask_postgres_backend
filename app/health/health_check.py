import os

import boto3
import requests
from botocore.client import Config as boto_config
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from app.core.extensions import db
from app.services.redis_service import redis_conn
from config import Config


def redis_available():
    redis_conn.client()
    return True, "redis is ok"


def postgres_available():
    try:
        result = db.engine.execute("SELECT 1")
        if result:
            return True, "database is ok"
    except Exception as e:
        return False, str(e)


HEALTH_CHECKS = [
    redis_available,
    postgres_available
]
