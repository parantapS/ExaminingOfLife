from fastapi import APIRouter
from backend.app.models.schemas import ChatRequest, ChatResponse
from backend.app.services.llm_service import call_llm

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/openai", response_model=ChatResponse)
async def chat_with_openai(payload: ChatRequest):
    reply = await call_llm(
        model="openai/gpt-4o-mini",
        system_prompt="You are a thoughtful philosopher.",
        user_message=payload.message,
    )
    return ChatResponse(reply=reply)
