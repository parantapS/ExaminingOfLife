from fastapi import APIRouter
from backend.app.services.chatroom_service import ChatRoom

router = APIRouter(prefix="/chatroom", tags=["chatroom"])

chatroom = ChatRoom()

@router.post("/input")
async def send_input(text: str):
    await chatroom.run_turn(text)
    return chatroom.get_history()

