import httpx
from backend.app.core.config import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def call_llm(
    model: str,
    system_prompt: str,
    user_message: str,
):
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"]
    

def build_llm_messages(history, system_prompt):
    messages = [{"role": "system", "content": system_prompt}]

    for msg in history:
        if msg.role == "human":
            messages.append({"role": "user", "content": msg.content})
        else:
            messages.append({"role": "assistant", "content": msg.content})

    return messages



