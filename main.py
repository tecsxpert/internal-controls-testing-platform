from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "AI service running"}

@app.post("/ai")
def ai_response(request: AIRequest):
    user_text = request.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_text}
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}