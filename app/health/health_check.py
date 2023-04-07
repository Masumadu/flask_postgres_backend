from app.core.extensions import db
from app.services.redis_service import redis_conn


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


HEALTH_CHECKS = [redis_available, postgres_available]
