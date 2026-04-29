from flask import Blueprint, request, jsonify
from datetime import datetime
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

recommend_bp = Blueprint('recommend', __name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data or "input" not in data:
        return jsonify({"error": "input field is required"}), 400

    input_text = data["input"].strip()

    if not input_text:
        return jsonify({"error": "input cannot be empty"}), 400

    with open("prompts/recommend.txt", "r") as f:
        prompt_template = f.read()

    prompt = prompt_template.replace("{input}", input_text)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        result = response.choices[0].message.content
        return jsonify({
            "recommendations": result,
            "generated_at": datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "error": "AI service failed",
            "is_fallback": True,
            "generated_at": datetime.utcnow().isoformat()
        }), 500