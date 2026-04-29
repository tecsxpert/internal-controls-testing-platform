from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import process_prompt

router = APIRouter()

class PromptRequest(BaseModel):
    text: str

@router.post("/ai")
def ai_response(request: PromptRequest):
    result = process_prompt(request.text)
    return {"response": result}