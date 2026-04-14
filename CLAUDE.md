# brush-up-py

A Python teaching agent built on a Zettelkasten-style knowledge graph.

## Architecture

- **`notes/`** — 127 atomic markdown notes about Python concepts, interconnected via `[[wikilinks]]`
- **`src/graph.py`** — Parses notes into a NetworkX `DiGraph`. Nodes carry note content, edges represent wikilinks. Provides 1-hop context gathering and TF-IDF retrieval (`TfidfIndex`)
- **`src/agent.py`** — Teaching agent. Finds the relevant topic from a user question, gathers 1-hop graph context, builds a system prompt (from `tutor_prompt.md` + context), calls Claude API, and returns token usage
- **`src/main.py`** — Interactive CLI chat loop
- **`src/api.py`** — FastAPI backend exposing chat and health endpoints
- **`src/budget.py`** — In-memory per-user token budget tracking (no persistence, resets on restart)
- **`tutor_prompt.md`** — Socratic tutor system prompt (do not modify without user approval)

## Development

```bash
source .venv/bin/activate
uv pip install -e ".[dev]"    # uses uv, not pip directly
.venv/bin/pytest -v
```

- Python 3.13, managed by uv
- Tests use pytest; agent tests mock the Anthropic client via dependency injection
- Graph tests use a `mini_notes` fixture (6 temp files in `tmp_path`), never the real corpus
- API tests use FastAPI `TestClient` and in-memory budget dicts

If you need the web stack locally:

```bash
uv pip install -e ".[dev,web]"
```

## Running

```bash
ANTHROPIC_API_KEY=... python src/main.py
```

```bash
ANTHROPIC_API_KEY=... uvicorn api:app --app-dir src --port 8080
```

## Key decisions

- Self-referential wikilinks are excluded from graph edges (no self-loops)
- Duplicate wikilinks from the same note produce only one edge
- Dangling links (to notes that don't exist) are silently ignored
- `TfidfIndex` provides content-based retrieval with title boosting and wikilink-aware tokenization
- The tutor prompt is loaded once at module import from `tutor_prompt.md`
- Model is configured in `src/agent.py` via `BRUSH_UP_MODEL`, defaulting to Sonnet 4
- `ask(...)` returns `(response_text, updated_history, usage_dict)`
- Conversation history is passed in by the caller; the backend does not persist chat history server-side
- Per-user token budget is tracked in-memory via `src/budget.py` (250K input / 60K output defaults, configurable via env vars)
- No rate limiting — budget tracking is the sole abuse-control mechanism
- Identity is a frontend-generated UUID in localStorage; ephemeral by design
