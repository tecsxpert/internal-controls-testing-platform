from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import time
from groq import Groq
from dotenv import load_dotenv
from services.cache import get_cached_response, set_cached_response, record_response_time

load_dotenv()

describe_bp = Blueprint('describe', __name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@describe_bp.route("/describe", methods=["POST"])
def describe():
    data = request.get_json()

    # Validate input
    if not data or "input" not in data:
        return jsonify({"error": "input field is required"}), 400
    
    input_text = data["input"].strip()
    
    if not input_text:
        return jsonify({"error": "input cannot be empty"}), 400

    # Check cache first
    cached = get_cached_response("describe:" + input_text)
    if cached:
        cached["from_cache"] = True
        return jsonify(cached), 200

    # Load prompt template
    with open("prompts/describe.txt", "r") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.replace("{input}", input_text)

    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        duration = time.time() - start_time
        record_response_time(duration)
        
        result = response.choices[0].message.content
        
        response_data = {
            "result": result,
            "generated_at": datetime.utcnow().isoformat(),
            "response_time_seconds": round(duration, 3)
        }

        set_cached_response("describe:" + input_text, response_data)
        
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            "error": "AI service temporarily unavailable",
            "is_fallback": True,
            "result": "Unable to generate description at this time. Please try again later.",
            "generated_at": datetime.utcnow().isoformat()
        }), 500