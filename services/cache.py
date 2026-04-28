import redis
import hashlib
import json

# Connect to Redis
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    redis_available = True
except:
    redis_client = None
    redis_available = False

def get_cache_key(input_text):
    return hashlib.sha256(input_text.encode()).hexdigest()

def get_cached_response(input_text):
    if not redis_available:
        return None
    try:
        key = get_cache_key(input_text)
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None
    except:
        return None

def set_cached_response(input_text, response):
    if not redis_available:
        return
    try:
        key = get_cache_key(input_text)
        redis_client.setex(key, 900, json.dumps(response))  # 900 seconds = 15 min TTL
    except:
        pass