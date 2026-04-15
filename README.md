# Brush up python backend

Backend for [Brush Up Python](https://www.joecardoso.dev/brush-up-py), a small AI-powered Python tutor built to showcase applied product and engineering work.

The app answers Python questions by grounding model responses in a personal Zettelkasten-style knowledge base of interconnected markdown notes. This repository contains the backend API, retrieval pipeline, tutor prompt, and test suite.

## What this does

- Serves a FastAPI chat API for the public brush-up-py frontend
- Builds a directed knowledge graph from markdown notes in `notes/`
- Retrieves the most relevant topic with a lightweight TF-IDF index
- Expands context with 1-hop graph neighbors before calling Anthropic
- Tracks per-user token usage in memory to limit abuse on the public demo

## Architecture

### Flow

1. A user asks a Python question from the frontend.
2. The backend scores the question against the note corpus with TF-IDF retrieval.
3. The top matching note becomes the primary topic.
4. The graph expands that topic with connected neighbor notes.
5. The backend builds a grounded system prompt from `tutor_prompt.md` plus the retrieved note context.
6. Anthropic generates the tutoring response.
7. The API returns the response, updated conversation history, and token usage metadata.

### Main pieces

- `src/api.py`  
  FastAPI app with `/api/chat` and `/api/health`, app startup lifecycle, CORS config, and API error handling.

- `src/agent.py`  
  Retrieval-aware tutoring logic. Selects context, assembles the system prompt, calls Anthropic, and returns usage metadata.

- `src/graph.py`  
  Builds a `networkx.DiGraph` from Obsidian-style `[[wikilinks]]`, exposes 1-hop context gathering, and implements the TF-IDF search index.

- `src/budget.py`  
  In-memory per-user input/output token budget tracking.

- `src/main.py`  
  Simple CLI entrypoint for chatting with the tutor locally.

- `notes/`  
  The teaching corpus: atomic markdown notes on Python concepts with wikilinks between them.

- `tutor_prompt.md`  
  The tutor's behavioral/system prompt.

## Tech stack

- Python 3.11+
- FastAPI
- NetworkX
- Anthropic Python SDK
- pytest
- uv for environment and dependency management
- Fly.io for deployment

## Local development

### Prerequisites

- Python 3.11 or newer
- `uv`
- `ANTHROPIC_API_KEY`

### Install dependencies

```bash
uv pip install -e ".[dev,web]"
```

If you only want the core package plus tests:

```bash
uv pip install -e ".[dev]"
```

### Run the API

```bash
ANTHROPIC_API_KEY=your_key uvicorn api:app --app-dir src --reload --port 8080
```

### Run the CLI

```bash
ANTHROPIC_API_KEY=your_key python src/main.py
```

### Run tests

```bash
uv run pytest
```

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | none | Required for model calls |
| `BRUSH_UP_MODEL` | `claude-sonnet-4-20250514` | Anthropic model used by the tutor |
| `BRUSH_UP_INPUT_BUDGET` | `250000` | Per-user input token cap |
| `BRUSH_UP_OUTPUT_BUDGET` | `60000` | Per-user output token cap |
| `BRUSH_UP_ALLOWED_ORIGINS` | built-in allowlist | Comma-separated CORS origins |
| `BRUSH_UP_ALLOWED_ORIGIN_REGEX` | `^https://[-a-zA-Z0-9]+\.vercel\.app$` | Regex-based CORS allowlist |

## API

### `POST /api/chat`

Request body:

```json
{
  "user_id": "browser-generated-id",
  "question": "What is a Python list comprehension?",
  "conversation_history": []
}
```

Response body:

```json
{
  "response": "A list comprehension is ...",
  "history": [
    { "role": "user", "content": "What is a Python list comprehension?" },
    { "role": "assistant", "content": "A list comprehension is ..." }
  ],
  "usage": {
    "input_tokens": 123,
    "output_tokens": 456,
    "retrieval": {
      "topic": "Comprehension",
      "score": 0.73,
      "neighbors": 4
    }
  }
}
```

Behavior notes:

- Returns `429` when a user exceeds the in-memory token budget
- Returns `503` when Anthropic reports temporary overload
- Returns `502` for other Anthropic API failures
- Does not persist conversation history server-side; the client sends it back on each request

### `GET /api/health`

Returns service status plus the number of topics loaded into the graph.

## Deployment

This repo includes:

- `Dockerfile` for containerized deployment
- `fly.toml` for Fly.io

The production container:

- installs the web dependencies
- copies `src/`, `notes/`, and `tutor_prompt.md`
- runs `uvicorn` on port `8080`

## Testing

The project includes unit, integration, and API-level tests covering the graph builder, retrieval, tutor flow, budget logic, and FastAPI endpoints.

## License

[MIT](./LICENSE)
