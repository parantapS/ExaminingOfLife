from fastapi import FastAPI
from backend.app.api.chat import router as chat_router
from backend.app.api.chatroom import router as chatroom_router

app = FastAPI(title="Examining of Life")

app.include_router(chat_router)
app.include_router(chatroom_router)

@app.get("/")
async def health_check():
    return {"status": "ok"}
