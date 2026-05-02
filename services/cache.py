import redis
import hashlib
import json
import time

# Connect to Redis
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    redis_available = True
except:
    redis_client = None
    redis_available = False

# Track response times
response_times = []

def record_response_time(duration):
    response_times.append(duration)
    if len(response_times) > 100:
        response_times.pop(0)

def get_avg_response_time():
    if not response_times:
        return 0
    return round(sum(response_times) / len(response_times), 3)

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
        redis_client.setex(key, 900, json.dumps(response))
    except:
        pass