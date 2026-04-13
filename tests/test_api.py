"""Tests for api.py — FastAPI endpoints with mocked Claude client."""

from contextlib import asynccontextmanager
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from db import init_db, record_usage, get_usage
from graph import build_graph


def _make_mock_client(response_text="Here is my explanation."):
    """Create a mock Anthropic client that returns a canned response."""
    client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=response_text)]
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 50
    client.messages.create.return_value = mock_response
    return client


@pytest.fixture
def app_client(mini_notes):
    """Create a TestClient with test graph, mock Claude client, and in-memory DB."""
    import api

    test_graph = build_graph(mini_notes)
    mock_client = _make_mock_client()
    test_db = init_db(":memory:")

    @asynccontextmanager
    async def test_lifespan(app):
        yield

    api.app.router.lifespan_context = test_lifespan

    with TestClient(api.app, raise_server_exceptions=True) as client:
        api.app.state.graph = test_graph
        api.app.state.client = mock_client
        api.app.state.db = test_db
        yield client, mock_client, test_db


# ── Group M: POST /api/chat ───────────────────────────────────────────


class TestChat:
    def test_returns_response(self, app_client):
        client, _, _ = app_client
        resp = client.post("/api/chat", json={
            "user_id": "test-user",
            "question": "What is Alpha?",
            "conversation_history": [],
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "response" in data
        assert "history" in data
        assert "usage" in data
        assert data["response"] == "Here is my explanation."

    def test_records_usage_in_db(self, app_client):
        client, _, test_db = app_client
        client.post("/api/chat", json={
            "user_id": "test-user",
            "question": "What is Alpha?",
            "conversation_history": [],
        })
        usage = get_usage(test_db, "test-user")
        assert usage["total_input_tokens"] == 100
        assert usage["total_output_tokens"] == 50

    def test_budget_exceeded(self, app_client):
        client, _, test_db = app_client
        record_usage(test_db, "big-spender", 9999999, 9999999)
        resp = client.post("/api/chat", json={
            "user_id": "big-spender",
            "question": "What is Alpha?",
            "conversation_history": [],
        })
        assert resp.status_code == 429
        assert resp.json()["error"] == "budget_exceeded"

    def test_empty_question_rejected(self, app_client):
        client, _, _ = app_client
        resp = client.post("/api/chat", json={
            "user_id": "test-user",
            "question": "",
            "conversation_history": [],
        })
        assert resp.status_code == 422

    def test_missing_user_id_rejected(self, app_client):
        client, _, _ = app_client
        resp = client.post("/api/chat", json={
            "question": "What is Alpha?",
            "conversation_history": [],
        })
        assert resp.status_code == 422

    def test_calls_claude_api(self, app_client):
        client, mock_claude, _ = app_client
        client.post("/api/chat", json={
            "user_id": "test-user",
            "question": "What is Alpha?",
            "conversation_history": [],
        })
        mock_claude.messages.create.assert_called_once()

    def test_passes_conversation_history(self, app_client):
        client, mock_claude, _ = app_client
        history = [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello!"},
        ]
        client.post("/api/chat", json={
            "user_id": "test-user",
            "question": "What is Alpha?",
            "conversation_history": history,
        })
        call_kwargs = mock_claude.messages.create.call_args.kwargs
        messages = call_kwargs["messages"]
        assert len(messages) == 3
        assert messages[0] == {"role": "user", "content": "Hi"}


# ── Group N: GET /api/health ──────────────────────────────────────────


class TestHealth:
    def test_returns_ok(self, app_client):
        client, _, _ = app_client
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["topics"] == 6  # mini_notes has 6 files


# ── Group O: GET /api/usage ───────────────────────────────────────────


class TestUsage:
    def test_returns_zeros_for_unknown_user(self, app_client):
        client, _, _ = app_client
        resp = client.get("/api/usage/nobody")
        assert resp.status_code == 200
        assert resp.json()["total_input_tokens"] == 0

    def test_returns_actual_usage(self, app_client):
        client, _, test_db = app_client
        record_usage(test_db, "test-user", 500, 200)
        resp = client.get("/api/usage/test-user")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_input_tokens"] == 500
        assert data["total_output_tokens"] == 200


# ── Group P: CORS ─────────────────────────────────────────────────────


class TestCors:
    @pytest.mark.parametrize(
        "origin",
        [
            "https://joecardoso.dev",
            "https://www.joecardoso.dev",
            "http://localhost:4321",
            "https://brush-up-py-git-main-joe.vercel.app",
        ],
    )
    def test_preflight_allows_configured_origins(self, app_client, origin):
        client, _, _ = app_client

        resp = client.options(
            "/api/chat",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        assert resp.status_code == 200
        assert resp.headers["access-control-allow-origin"] == origin

    def test_preflight_rejects_unknown_origin(self, app_client):
        client, _, _ = app_client

        resp = client.options(
            "/api/chat",
            headers={
                "Origin": "https://evil.example",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        assert resp.status_code == 400
        assert "access-control-allow-origin" not in resp.headers
