YOUTUBE_KEY = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"

CACHE_TIMEOUT_MS = 10000
INGESTOR_REWIND_MINUTES = 5
INGESTOR_INTERVAL_SECONDS = 30
DEFAULT_PAGE_OFFSET = 0
DEFAULT_PAGE_SIZE = 30

flask_app_config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "redis",
    "CACHE_KEY_PREFIX": "request-",
    "CACHE_REDIS_PORT": 6379
}