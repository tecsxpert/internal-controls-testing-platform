import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app = Flask(__name__)

# Hide Werkzeug server info
import werkzeug.serving
werkzeug.serving.WSGIRequestHandler.server_version = ""
werkzeug.serving.WSGIRequestHandler.sys_version = ""

# ── Rate Limiter — 30 requests/min per IP ───────────────────
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

# ── Security Headers ─────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'; object-src 'none'"
    response.headers['Server'] = 'Flask'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# ── Register blueprints ──────────────────────────────────────
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp

app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)

# ── Health check ─────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok', 'model': 'llama-3.3-70b'}, 200

# ── Rate limit error handler ─────────────────────────────────
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return {
        "error": "Rate limit exceeded",
        "message": "Maximum 30 requests per minute allowed",
        "code": 429
    }, 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)