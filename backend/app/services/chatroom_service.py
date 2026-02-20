from typing import List
from backend.app.models.messages import ChatMessage
from backend.app.core.personas import NIETZSCHE_PROMPT, DOSTOEVSKY_PROMPT
from backend.app.services.llm_service import call_llm, build_llm_messages
from backend.app.core.conversation_mode import ConversationMode
from backend.app.services.command_parser import parse_command

MAX_DEBATE_TURNS = 2

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

    def add_message(self, role: str, content: str):
        self.history.append(ChatMessage(role=role, content=content))

    def get_history(self) -> List[ChatMessage]:
        return self.history
    
    async def respond_nietzsche(self):
        reply = await call_llm(
            model="anthropic/claude-3-5-sonnet",
            messages=build_llm_messages(self.history, NIETZSCHE_PROMPT, speaking_agent="nietzsche"),
        )
        if reply and reply.strip():
            self.add_message("nietzsche", reply)

    async def respond_dostoevsky(self):
        reply = await call_llm(
            model="openai/gpt-4o-mini",
            messages=build_llm_messages(self.history, DOSTOEVSKY_PROMPT, speaking_agent="dostoevsky"),
        )
        if reply and reply.strip():
            self.add_message("dostoevsky", reply)
        

    async def run_turn(self, text: str):
        command_type, mode, content = parse_command(text)

        # Mode-only commands
        if command_type == "mode":
            self.set_mode(mode)
            return

        # Direct question to one agent
        if command_type == "direct":
            self.set_mode(mode)
            self.add_message("human", content)

            if mode == ConversationMode.HUMAN_TO_NIETZSCHE:
                await self.respond_nietzsche()
                return

            if mode == ConversationMode.HUMAN_TO_DOSTOEVSKY:
                await self.respond_dostoevsky()
                return

        # Debate command
        if command_type == "debate":
            self.set_mode(mode)
            self.add_message("human", content)

            for _ in range(MAX_DEBATE_TURNS):
                await self.respond_dostoevsky()
                await self.respond_nietzsche()
            return

        # Normal human input
        self.add_message("human", content)

        if self.mode == ConversationMode.PAUSED:
            return

        if self.mode == ConversationMode.HUMAN_TO_ALL:
            await self.respond_dostoevsky()
            await self.respond_nietzsche()

