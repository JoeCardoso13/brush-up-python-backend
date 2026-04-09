# brush-up-py

A Python teaching agent built on a Zettelkasten-style knowledge graph.

## Architecture

- **`notes/`** — 127 atomic markdown notes about Python concepts, interconnected via `[[wikilinks]]`
- **`src/graph.py`** — Parses notes into a NetworkX `DiGraph`. Nodes carry note content, edges represent wikilinks. Provides 1-hop context gathering and fuzzy topic matching (`difflib`)
- **`src/agent.py`** — Teaching agent. Finds the relevant topic from a user question, gathers 1-hop graph context, builds a system prompt (from `tutor_prompt.md` + context), calls Claude API, and returns token usage
- **`src/main.py`** — Interactive CLI chat loop
- **`src/api.py`** — FastAPI backend exposing chat, health, and usage endpoints
- **`src/db.py`** — SQLite-backed per-user token budget tracking
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
- API tests use FastAPI `TestClient` and in-memory SQLite

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
- `find_topic` does exact case-insensitive match first, then `difflib.get_close_matches` (cutoff 0.6)
- The tutor prompt is loaded once at module import from `tutor_prompt.md`
- Model is configured in `src/agent.py` via `BRUSH_UP_MODEL`, defaulting to Sonnet 4
- `ask(...)` returns `(response_text, updated_history, usage_dict)`
- Conversation history is passed in by the caller; the backend does not persist chat history server-side
- Per-user token usage is tracked in SQLite via `src/db.py`
