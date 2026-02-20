from backend.app.core.conversation_mode import ConversationMode

def parse_command(text: str):
    text = text.strip()

    if text.startswith("/ask nietzsche"):
        return (
            "direct",
            ConversationMode.HUMAN_TO_NIETZSCHE,
            text.replace("/ask nietzsche", "").strip(),
        )

    if text.startswith("/ask dostoevsky"):
        return (
            "direct",
            ConversationMode.HUMAN_TO_DOSTOEVSKY,
            text.replace("/ask dostoevsky", "").strip(),
        )

    if text.startswith("/debate"):
        return (
            "debate",
            ConversationMode.DEBATE,
            text.replace("/debate", "").strip(),
        )

    if text == "/pause":
        return ("mode", ConversationMode.PAUSED, None)

    if text == "/resume":
        return ("mode", ConversationMode.HUMAN_TO_ALL, None)

    return (None, None, text)
