from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "model": "llama-3.3-70b"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)