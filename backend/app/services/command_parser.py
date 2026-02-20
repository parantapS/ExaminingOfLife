from backend.app.core.conversation_mode import ConversationMode

def parse_command(text: str):
    text = text.strip().lower()

    if text == "/pause":
        return ("mode", ConversationMode.PAUSED)

    if text == "/resume":
        return ("mode", ConversationMode.HUMAN_TO_ALL)

    if text == "/debate":
        return ("mode", ConversationMode.DEBATE)

    if text == "/ask nietzsche":
        return ("mode", ConversationMode.HUMAN_TO_NIETZSCHE)

    if text == "/ask dostoevsky":
        return ("mode", ConversationMode.HUMAN_TO_DOSTOEVSKY)

    return (None, None)
