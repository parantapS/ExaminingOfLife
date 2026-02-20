# the messages that are sent to the LLM, but this is app's language, not LLM's language
from pydantic import BaseModel
from typing import Literal

class ChatMessage(BaseModel):
    role: Literal[
        "human",
        "nietzsche",
        "dostoevsky",
        "system"
    ]
    content: str
