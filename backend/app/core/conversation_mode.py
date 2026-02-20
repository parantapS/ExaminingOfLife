# my governer, to prevent the LLM from hallucinating or generating responses that are not consistent with the history of the conversation
from enum import Enum

class ConversationMode(str, Enum):
    PAUSED = "paused"
    HUMAN_TO_ALL = "human_to_all"
    HUMAN_TO_NIETZSCHE = "human_to_nietzsche"
    HUMAN_TO_DOSTOEVSKY = "human_to_dostoevsky"
    DEBATE = "debate"
