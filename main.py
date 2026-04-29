from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class AIRequest(BaseModel):
    text: str

# Root endpoint
@app.get("/")
def root():
    return {"message": "AI service running"}

# AI endpoint (mock response - works without API key)
@app.post("/ai")
def ai_response(request: AIRequest):
    user_text = request.text

    # Simple logic (you can enhance later)
    return {
        "response": f"You said: {user_text}"
    }