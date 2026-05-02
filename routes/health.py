from flask import Blueprint, jsonify
import time
import os
from services.cache import get_avg_response_time, redis_available

health_bp = Blueprint('health', __name__)

# Track start time for uptime
start_time = time.time()

@health_bp.route("/health", methods=["GET"])
def health():
    uptime_seconds = int(time.time() - start_time)

    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "avg_response_time_seconds": get_avg_response_time(),
        "uptime_seconds": uptime_seconds,
        "redis_available": redis_available
    }), 200