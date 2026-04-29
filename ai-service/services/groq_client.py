import os
import time
import json
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── Logging setup ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────
MAX_RETRIES = 3
BACKOFF_SECONDS = [1, 2, 4]
MODEL = "llama-3.3-70b-versatile"


class GroqClient:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        self.client = Groq(api_key=api_key)
        logger.info("GroqClient initialised successfully")

    def call(self, system_prompt: str, user_prompt: str,
             temperature: float = 0.3, max_tokens: int = 1000) -> dict:
        """
        Call Groq API with 3-retry + exponential backoff.
        Always returns a dict — never raises to the caller.
        """
        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"Groq API call — attempt {attempt}/{MAX_RETRIES}")

                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                raw_text = response.choices[0].message.content
                logger.info(f"Groq API call succeeded on attempt {attempt}")
                logger.info(f"Tokens used: {response.usage.total_tokens}")

                return self._parse_response(raw_text)

            except Exception as e:
                last_error = e
                logger.error(f"Attempt {attempt} failed: {e}")

                if attempt < MAX_RETRIES:
                    wait = BACKOFF_SECONDS[attempt - 1]
                    logger.info(f"Retrying in {wait}s...")
                    time.sleep(wait)

        # All retries exhausted — return fallback
        logger.error(f"All {MAX_RETRIES} attempts failed. Returning fallback.")
        return self._fallback(str(last_error))

    def _parse_response(self, raw_text: str) -> dict:
        """
        Try to parse the model response as JSON.
        If it fails, wrap the plain text in a dict.
        """
        try:
            cleaned = raw_text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            return {
                "success": True,
                "is_fallback": False,
                "data": json.loads(cleaned)
            }
        except (json.JSONDecodeError, IndexError):
            return {
                "success": True,
                "is_fallback": False,
                "data": {"text": raw_text}
            }

    def _fallback(self, error_message: str) -> dict:
        """
        Returned when all retries fail.
        Never returns HTTP 500 — always a safe fallback.
        """
        return {
            "success": False,
            "is_fallback": True,
            "error": error_message,
            "data": {
                "text": "AI service is temporarily unavailable. Please try again later."
            }
        }
    
if __name__ == "__main__":
    client = GroqClient()
    result = client.call(
        system_prompt="You are an internal controls audit assistant.",
        user_prompt="List 2 risks in accounts payable. Reply in JSON with a 'risks' array."
    )
    print(result)