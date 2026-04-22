import bleach
import re
from flask import request, jsonify
from functools import wraps

# ── Prompt injection patterns ────────────────────────────────
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all instructions",
    r"disregard previous",
    r"forget previous",
    r"you are now",
    r"act as",
    r"pretend you are",
    r"pretend to be",
    r"you will now",
    r"override instructions",
    r"system prompt",
    r"reveal your prompt",
    r"print your instructions",
    r"what are your instructions",
]


def sanitise_text(text: str) -> str:
    """Strip all HTML tags from input text."""
    return bleach.clean(text, tags=[], strip=True).strip()


def is_prompt_injection(text: str) -> bool:
    """Check if the text contains prompt injection patterns."""
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def sanitise_input(f):
    """
    Decorator — sanitises all string fields in the request JSON.
    Returns 400 if prompt injection is detected.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            data = request.get_json()

            if data:
                for key, value in data.items():
                    if isinstance(value, str):
                        # Check for injection before sanitising
                        if is_prompt_injection(value):
                            return jsonify({
                                "error": "Invalid input detected",
                                "field": key,
                                "code": 400
                            }), 400
                        # Strip HTML
                        data[key] = sanitise_text(value)

                # Replace request data with sanitised version
                request.sanitised_data = data

        return f(*args, **kwargs)
    return decorated_function