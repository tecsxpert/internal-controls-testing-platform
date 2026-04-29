from flask import Blueprint, jsonify
import time
import os
import redis

health_bp = Blueprint('health', __name__)

# Track start time for uptime
start_time = time.time()

# Response times tracker
response_times = []

# Connect to Redis (gracefully handle if not running)
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    redis_available = True
except:
    redis_client = None
    redis_available = False

@health_bp.route("/health", methods=["GET"])
def health():
    uptime_seconds = int(time.time() - start_time)
    
    avg_response_time = (
        round(sum(response_times) / len(response_times), 3)
        if response_times else 0
    )

    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "avg_response_time_seconds": avg_response_time,
        "uptime_seconds": uptime_seconds,
        "redis_available": redis_available
    }), 200