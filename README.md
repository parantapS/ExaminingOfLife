# Examining of Life

A multi-LLM chatroom backend that connects to the **Open Router API** to call various language models. The project is structured in phases; **Phase One** delivers a minimal AI backend using **GPT-4o-mini** via Open Router.

---

## Phase One

Phase One focuses on:

- A **FastAPI** backend with a single chat endpoint
- Integration with **Open Router** (`https://openrouter.ai/api/v1/chat/completions`)
- Using the **openai/gpt-4o-mini** model for chat completions
- Request/response validation with **Pydantic**
- Environment-based configuration for the API key

---

## Phase 2.1

Phase 2.1 adds a **multi-model chatroom** foundation:

- **Chatroom API** — `POST /chatroom/input` endpoint for conversation-style input
- **Conversation modes** — `PAUSED`, `HUMAN_TO_ALL`, `HUMAN_TO_NIETZSCHE`, `HUMAN_TO_DOSTOEVSKY`, `DEBATE`
- **Slash commands** — `/pause`, `/resume`, `/debate`, `/ask nietzsche`, `/ask dostoevsky`
- **ChatMessage model** — Message roles: `human`, `nietzsche`, `dostoevsky`, `system`
- **Personas** — Nietzsche and Dostoevsky philosopher personas (for future LLM integration)
- **Command parser** — Parses user input into mode changes vs regular messages
- **build_llm_messages** — Helper in `llm_service` to convert chat history to LLM format

---

## Phase 2.2

Phase 2.2 adds **full LLM integration** to the chatroom:

- **Live philosopher responses** — Nietzsche and Dostoevsky personas now call real LLMs:
  - **Nietzsche** uses `anthropic/claude-3-5-sonnet`
  - **Dostoevsky** uses `openai/gpt-4o-mini`
- **`run_turn`** — Main orchestration that processes user input, slash commands, and triggers LLM responses
- **Direct questions** — `/ask nietzsche` and `/ask dostoevsky` send the question to that persona and get an LLM reply
- **Debate mode** — `/debate` triggers alternating responses from both philosophers (4 turns each)
- **HUMAN_TO_ALL** — When in human-to-all mode, both philosophers respond to each human message (Dostoevsky first, then Nietzsche)
- **`respond_nietzsche()` / `respond_dostoevsky()`** — Async methods that call Open Router with persona prompts and append replies to history
- **`build_llm_messages`** — Converts chat history to Open Router format with persona-specific system prompts

---

## Tech Stack

| Component        | Technology                                               |
|-----------------|----------------------------------------------------------|
| Web framework   | FastAPI                                                  |
| HTTP client     | httpx (async)                                            |
| Config / env     | python-dotenv                                            |
| Server          | Uvicorn                                                  |
| LLM gateway     | Open Router API                                          |
| Models          | openai/gpt-4o-mini, anthropic/claude-3-5-sonnet          |

---

## Project Tree Structure

```
examiningoflife/
├── .env                    # Environment variables (OPENROUTER_API_KEY); not committed
├── .gitignore
├── .python-version         # Python version (e.g. 3.12)
├── README.md               # This file
├── main.py                 # Optional top-level entry (e.g. "Hello from examiningoflife!")
├── pyproject.toml          # Project metadata and dependencies (uv/pip)
├── uv.lock                 # Locked dependency versions
│
├── backend/
│   └── app/
│       ├── main.py         # FastAPI app, router registration, health check
│       ├── api/
│       │   ├── chat.py     # Chat API routes (/chat/openai)
│       │   └── chatroom.py # Chatroom API routes (/chatroom/input)
│       ├── core/
│       │   ├── config.py           # Settings and env loading (OPENROUTER_API_KEY)
│       │   ├── conversation_mode.py # ConversationMode enum
│       │   └── personas.py         # Philosopher personas (Nietzsche, Dostoevsky)
│       ├── models/
│       │   ├── schemas.py  # Pydantic models: ChatRequest, ChatResponse
│       │   └── messages.py # ChatMessage model for chatroom
│       └── services/
│           ├── llm_service.py      # Open Router API client (call_llm, build_llm_messages)
│           ├── chatroom_service.py # ChatRoom state, mode switching, history
│           └── command_parser.py   # Slash command parsing
│
└── frontend/               # Reserved for future frontend
```

- **`backend/app/main.py`** — Creates the FastAPI app, mounts the chat router, and defines the root health check.
- **`backend/app/api/chat.py`** — Defines the chat endpoint and delegates to the LLM service.
- **`backend/app/core/config.py`** — Loads `.env` and exposes `settings.OPENROUTER_API_KEY`.
- **`backend/app/models/schemas.py`** — Request/response shapes for the chat API.
- **`backend/app/services/llm_service.py`** — Sends requests to Open Router and returns the assistant message content.

---

## Routing

All HTTP routes are defined in the FastAPI app in `backend/app/main.py` and the chat router in `backend/app/api/chat.py`.

| Method | Path              | Description |
|--------|-------------------|-------------|
| `GET`  | `/`               | Health check. Returns `{"status": "ok"}`. |
| `POST` | `/chat/openai`    | Chat with the AI. Body: `{"message": "your text"}`. Returns `{"reply": "..."}`. |
| `POST` | `/chatroom/input` | Send input to chatroom. Query: `?text=...`. Accepts slash commands or human messages. Returns conversation history. |

- The **chat** router is registered with **prefix** `"/chat"` and **tags** `["chat"]`, so the full path for the current endpoint is **`/chat/openai`**.
- OpenAPI docs (Swagger UI): **`/docs`** when the server is running.
- ReDoc: **`/redoc`**.

---

## How It Works

1. **Request** — Client sends `POST /chat/openai` with a JSON body: `{"message": "Your question or prompt"}`.
2. **Validation** — FastAPI validates the body using the `ChatRequest` schema (`message: str`).
3. **LLM call** — The chat route calls `call_llm()` in `llm_service.py` with:
   - `model="openai/gpt-4o-mini"`
   - `system_prompt="You are a thoughtful philosopher."`
   - `user_message=payload.message`
4. **Open Router** — `llm_service` sends a POST request to `https://openrouter.ai/api/v1/chat/completions` with:
   - `Authorization: Bearer <OPENROUTER_API_KEY>`
   - JSON body: `model`, `messages` (system + user).
5. **Response** — The service reads `data["choices"][0]["message"]["content"]` and the route returns `ChatResponse(reply=...)`, i.e. `{"reply": "..."}`.

---

## Setup

### 1. Python and dependencies

- Python **3.12+** (see `.python-version`).
- From the project root, create a venv and install deps (e.g. with **uv**):

  ```bash
  uv sync
  ```

  Or with pip:

  ```bash
  pip install -e .
  ```

### 2. Environment variables

Create a **`.env`** file in the project root (it is gitignored):

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get an API key from [Open Router](https://openrouter.ai/).

---

## Running the Backend

From the **project root** (so that the `backend.app` package resolves correctly):

```bash
uvicorn backend.app.main:app --reload
```

- Server runs at **http://127.0.0.1:8000** by default.
- **`--reload`** restarts the server when code changes.

---

## Example API Usage

**Health check:**

```bash
curl http://127.0.0.1:8000/
```

**Chat (replace `YOUR_MESSAGE` with your text):**

```bash
curl -X POST http://127.0.0.1:8000/chat/openai \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the meaning of life?"}'
```

Example response:

```json
{"reply": "..."}
```

---

## Summary

- **Phase One** = FastAPI backend + Open Router + **gpt-4o-mini**, with one chat endpoint and a health check.
- **Phase 2.1** = Chatroom foundation with conversation modes, slash commands, personas, and `/chatroom/input` endpoint.
- **Phase 2.2** = Full LLM integration: Nietzsche (Claude) and Dostoevsky (GPT-4o-mini) respond live; direct questions, debate mode, and human-to-all conversations.
- **Project layout** = `backend/app` (main, api, core, models, services) plus config, schemas, personas, conversation modes.
- **Routing** = `GET /` (health), `POST /chat/openai` (chat), `POST /chatroom/input` (chatroom); docs at `/docs` and `/redoc`.
- **Config** = `OPENROUTER_API_KEY` in `.env`, loaded in `backend/app/core/config.py`.
