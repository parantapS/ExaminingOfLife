import httpx
from backend.app.core.config import settings
from backend.app.models.messages import ChatMessage

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def call_llm(model: str, messages: list[dict]) -> str:

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "examiningoflife",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        # response.raise_for_status()
        if response.status_code != 200:
            raise RuntimeError(
                f"OpenRouter error {response.status_code}: {response.text}"
            )
        print("OpenRouter response:", response.status_code, response.text)
        data = response.json()

    return data["choices"][0]["message"]["content"]

# History Translation (Boundary Layer)
def build_llm_messages(history: list[ChatMessage], system_prompt: str, speaking_agent: str):
    messages = [{"role": "system", "content": system_prompt}]

    for msg in history:
        if msg.role == "human":
            messages.append({"role": "user", "content": msg.content})
        elif msg.role == speaking_agent:
            messages.append({"role": "assistant", "content": msg.content})
        else:
            # Other agent messages appear as 'user' with label
            messages.append({
                "role": "user",
                "content": f"[{msg.role}]: {msg.content}"
            })

    return messages

# def build_llm_messages(
#     history: list[ChatMessage],
#     system_prompt: str,
# ):
#     messages = [{"role": "system", "content": system_prompt}]

#     for msg in history:
#         if msg.role == "human":
#             messages.append({"role": "user", "content": msg.content})
#         elif msg.role in ["nietzsche", "dostoevsky"]:
#             messages.append({"role": "assistant", "content": msg.content})

#     return messages



