from typing import List
from backend.app.models.messages import ChatMessage
# from backend.app.core.personas import OPENAI_PHILOSOPHER, CLAUDE_PHILOSOPHER
# from backend.app.services.llm_service import call_llm, build_llm_messages
from backend.app.core.conversation_mode import ConversationMode
from backend.app.services.command_parser import parse_command

class ChatRoom:
    def __init__(self):
        self.history: List[ChatMessage] = []
        self.mode: ConversationMode = ConversationMode.HUMAN_TO_ALL

        self.history.append(
            ChatMessage(
                role="system",
                content="Conversation initialized. Mode: HUMAN_TO_ALL."
            )
        )
    
    def set_mode(self, mode: ConversationMode):
        self.mode = mode
        self.history.append(
            ChatMessage(
                role="system",
                content=f"Conversation mode changed to: {mode.value}"
            )
        )

    def handle_input(self, text: str):
        command_type, value = parse_command(text)

        if command_type == "mode":
            self.set_mode(value)
            return

        # Normal human message
        self.add_message("human", text)

    def add_message(self, role: str, content: str):
        self.history.append(ChatMessage(role=role, content=content))

    def get_history(self) -> List[ChatMessage]:
        return self.history

    # may not be implemented

    # async def run_turn(self, human_input: str):
    #     self.add_message("human", human_input)

    #     openai_reply = await call_llm(
    #         model="openai/gpt-4o-mini",
    #         messages=build_llm_messages(self.history, OPENAI_PHILOSOPHER),
    #     )
    #     self.add_message("openai", openai_reply)

    #     claude_reply = await call_llm(
    #         model="anthropic/claude-3-5-sonnet",
    #         messages=build_llm_messages(self.history, CLAUDE_PHILOSOPHER),
    #     )
    #     self.add_message("claude", claude_reply)
