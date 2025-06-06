# Placeholder for ai_doc_summarizer/src/storage/redis_client.py
import logging
import redis
from src.utils.helpers import load_config

logger = logging.getLogger("ai_summarizer.redis_client")

class RedisClient:
    def __init__(self):
        cfg = load_config()
        host = cfg["redis"]["host"]
        port = cfg["redis"]["port"]
        password = cfg["redis"]["password"]
        db = cfg["redis"]["db"]
        self.client = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=True)

    def get(self, key: str):
        try:
            return self.client.get(key)
        except Exception as e:
            logger.error("Redis GET error: %s", e)
            return None

    def set(self, key: str, value, expire: int = 3600):
        try:
            self.client.set(name=key, value=value, ex=expire)
            logger.debug("Cached key: %s", key)
        except Exception as e:
            logger.error("Redis SET error: %s", e)
