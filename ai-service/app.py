import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ── App setup ────────────────────────────────────────────────
app = Flask(__name__)

# ── Rate Limiter — 30 requests/min per IP ───────────────────
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

# ── Health check ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "ai-service"}, 200


# ── Test sanitisation endpoint ───────────────────────────────
@app.route("/test-sanitise", methods=["POST"])
@limiter.limit("30 per minute")
def test_sanitise():
    from routes.sanitiser import sanitise_input
    from flask import request, jsonify

    @sanitise_input
    def inner():
        return jsonify({
            "message": "Input is clean",
            "received": request.sanitised_data
        }), 200

    return inner()


# ── Error handlers ───────────────────────────────────────────
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return {
        "error": "Rate limit exceeded",
        "message": "Maximum 30 requests per minute allowed",
        "code": 429
    }, 429


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)