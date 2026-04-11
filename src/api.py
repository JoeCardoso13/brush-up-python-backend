"""FastAPI backend for the brush-up-py Python tutor."""

import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

import anthropic
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from agent import ask
from db import init_db, check_budget, record_usage, get_usage
from graph import build_graph

logger = logging.getLogger("brush-up")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# ── Configuration ──────────────────────────────────────────────────────

NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"
DB_PATH = os.environ.get("BRUSH_UP_DB_PATH", "/data/brush_up.db")

ALLOWED_ORIGINS = [
    "https://joecardoso.dev",
    "http://localhost:4321",
]


# ── App lifecycle ──────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.graph = build_graph(NOTES_DIR)
    app.state.client = anthropic.Anthropic(max_retries=3)
    app.state.db = init_db(DB_PATH)
    logger.info("Graph loaded: %d topics", app.state.graph.number_of_nodes())
    yield


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="brush-up-py", docs_url=None, redoc_url=None, lifespan=lifespan)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "rate_limited", "detail": "Too many requests. Please slow down."},
    )


# ── Request / response models ──────────────────────────────────────────


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=2000)
    conversation_history: list[dict] = Field(default_factory=list, max_length=50)


class ChatResponse(BaseModel):
    response: str
    history: list[dict]
    usage: dict


# ── Endpoints ──────────────────────────────────────────────────────────


@app.post("/api/chat")
@limiter.limit("10/minute")
def chat(req: ChatRequest, request: Request):
    graph = request.app.state.graph
    client = request.app.state.client
    db = request.app.state.db

    if not check_budget(db, req.user_id):
        logger.info("budget exceeded user=%s", req.user_id[:8])
        return JSONResponse(
            status_code=429,
            content={
                "error": "budget_exceeded",
                "detail": "You've used your token allocation. Thanks for trying brush-up-py!",
            },
        )

    start = time.monotonic()
    try:
        response_text, updated_history, usage = ask(
            graph, req.question, req.conversation_history, client=client
        )
    except anthropic.APIStatusError as exc:
        if exc.status_code == 529:
            logger.warning("anthropic overloaded user=%s", req.user_id[:8])
            return JSONResponse(
                status_code=503,
                content={"error": "overloaded", "detail": "The AI service is temporarily busy. Please try again in a moment."},
            )
        logger.error("anthropic error user=%s: %s", req.user_id[:8], exc)
        return JSONResponse(
            status_code=502,
            content={"error": "api_error", "detail": "Something went wrong calling the AI service. Please try again."},
        )
    except anthropic.APIError as exc:
        logger.error("anthropic error user=%s: %s", req.user_id[:8], exc)
        return JSONResponse(
            status_code=502,
            content={"error": "api_error", "detail": "Something went wrong calling the AI service. Please try again."},
        )
    elapsed = time.monotonic() - start

    record_usage(db, req.user_id, usage["input_tokens"], usage["output_tokens"])

    logger.info(
        "chat user=%s q_len=%d tokens=%d+%d %.1fs",
        req.user_id[:8],
        len(req.question),
        usage["input_tokens"],
        usage["output_tokens"],
        elapsed,
    )

    return ChatResponse(response=response_text, history=updated_history, usage=usage)


@app.get("/api/health")
def health(request: Request):
    return {"status": "ok", "topics": request.app.state.graph.number_of_nodes()}


@app.get("/api/usage/{user_id}")
def usage(user_id: str, request: Request):
    db = request.app.state.db
    user_usage = get_usage(db, user_id)
    if user_usage is None:
        return {"total_input_tokens": 0, "total_output_tokens": 0}
    return user_usage
