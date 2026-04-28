from flask import Flask
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.health import health_bp
import os

load_dotenv()

app = Flask(__name__)

# Register blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)
app.register_blueprint(health_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)