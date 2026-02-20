from fastapi import APIRouter
from backend.app.services.chatroom_service import ChatRoom

router = APIRouter(prefix="/chatroom", tags=["chatroom"])

chatroom = ChatRoom()

@router.post("/input")
async def send_input(text: str):
    chatroom.handle_input(text)
    return chatroom.get_history()

# @router.post("/message")
# async def send_message(message: str):
#     await chatroom.run_turn(message)
#     return chatroom.get_history()
