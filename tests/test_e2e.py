"""End-to-end tests: HTTP request → real corpus retrieval → system prompt grounding.

These tests exercise the full stack through FastAPI's TestClient using the
real 127-note Zettelkasten corpus.  The Anthropic client is mocked (we're
testing retrieval grounding, not the LLM), but everything else is real:
request validation, middleware, the lifespan-built graph/index, TF-IDF
search, context gathering, and system prompt construction.

The key question: does the system prompt that reaches Claude actually contain
the right Zettelkasten content for a given user question?
"""

from contextlib import asynccontextmanager
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from graph import TfidfIndex


def _make_mock_client(response_text="Here is my explanation."):
    client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=response_text)]
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 50
    client.messages.create.return_value = mock_response
    return client


@pytest.fixture
def e2e_client(real_graph):
    """Full-stack TestClient backed by the real 127-note corpus.

    A fresh mock Anthropic client is created per test so call assertions
    are isolated.  The rate limiter is disabled to avoid 429s in tests.
    """
    import api

    mock_client = _make_mock_client()

    @asynccontextmanager
    async def test_lifespan(app):
        yield

    api.app.router.lifespan_context = test_lifespan

    with TestClient(api.app, raise_server_exceptions=True) as client:
        api.app.state.graph = real_graph
        api.app.state.index = TfidfIndex(real_graph)
        api.app.state.client = mock_client
        api.app.state.budgets = {}
        yield client, mock_client


def _chat(client, question, history=None):
    """Send a question through POST /api/chat and return (response_json, mock_client)."""
    return client.post("/api/chat", json={
        "user_id": "e2e-test-user",
        "question": question,
        "conversation_history": history or [],
    })


# ── Smoke: full chain works ───────────────────────────────────────


class TestE2ESmoke:
    def test_chat_returns_200(self, e2e_client):
        client, _ = e2e_client
        resp = _chat(client, "What is a for loop?")
        assert resp.status_code == 200
        data = resp.json()
        assert "response" in data
        assert "history" in data
        assert "usage" in data

    def test_retrieval_metadata_in_response(self, e2e_client):
        client, _ = e2e_client
        resp = _chat(client, "What is a for loop?")
        usage = resp.json()["usage"]
        assert "retrieval" in usage
        assert usage["retrieval"]["topic"] is not None
        assert usage["retrieval"]["score"] > 0
        assert usage["retrieval"]["neighbors"] >= 0


# ── Grounding: system prompt contains the right note ──────────────


class TestE2EGrounding:
    """For each question, verify that the system prompt passed to Claude
    contains content from the expected Zettelkasten note."""

    @pytest.mark.parametrize(
        "question, expected_topic, expected_content_snippet",
        [
            (
                "How does a for loop work?",
                "For loop",
                "for loop",
            ),
            (
                "What is a decorator?",
                "Decorator",
                "modify",
            ),
            (
                "Explain variable shadowing",
                "Variable shadowing",
                "syntactical difference",
            ),
            (
                "What is string interpolation?",
                "String interpolation",
                "interpolation",
            ),
            (
                "How does scope work in Python?",
                "Scope",
                "function scope",
            ),
            (
                "What is a dictionary?",
                "Dictionary",
                "dict",
            ),
            (
                "What is a list comprehension?",
                "Comprehension",
                "shorthand syntax",
            ),
            (
                "class definition blueprint",
                "Class",
                "class",
            ),
            (
                "What is encapsulation?",
                "Encapsulation",
                "encapsulation",
            ),
            (
                "What is polymorphism?",
                "Polymorphism",
                "polymorphism",
            ),
        ],
    )
    def test_grounding_correct_note(
        self, e2e_client, question, expected_topic, expected_content_snippet
    ):
        client, mock_claude = e2e_client
        mock_claude.reset_mock()
        resp = _chat(client, question)
        assert resp.status_code == 200

        # Verify retrieval metadata reports the right topic
        retrieval = resp.json()["usage"]["retrieval"]
        assert retrieval["topic"] == expected_topic, (
            f"Expected topic {expected_topic!r} but got {retrieval['topic']!r} "
            f"(score={retrieval['score']:.3f})"
        )

        # Verify the system prompt actually contains note content
        system_prompt = mock_claude.messages.create.call_args.kwargs["system"]
        assert expected_content_snippet in system_prompt.lower(), (
            f"Expected {expected_content_snippet!r} in system prompt for "
            f"topic {expected_topic!r}, but it wasn't there"
        )

    def test_system_prompt_has_no_wikilink_brackets(self, e2e_client):
        client, mock_claude = e2e_client
        mock_claude.reset_mock()
        _chat(client, "What is a for loop?")
        system_prompt = mock_claude.messages.create.call_args.kwargs["system"]
        assert "[[" not in system_prompt
        assert "]]" not in system_prompt

    def test_grounding_includes_neighbor_content(self, e2e_client):
        """The system prompt should contain not just the matched note,
        but also its graph neighbors — that's the Zettelkasten value."""
        client, mock_claude = e2e_client
        mock_claude.reset_mock()
        _chat(client, "What is a for loop?")
        system_prompt = mock_claude.messages.create.call_args.kwargs["system"]
        # For loop links to While, List, Sequence, etc — at least one neighbor
        # should appear as a separate section in the system prompt
        assert system_prompt.count("---") >= 2, (
            "System prompt should have multiple sections (topic + neighbors)"
        )


# ── Diverse phrasings through the full stack ──────────────────────


class TestE2EDiversePhrasings:
    """Same concept as integration TestDiversePhrasings, but through HTTP.
    This catches bugs where retrieval works in isolation but breaks when
    going through request parsing, the API layer, etc."""

    @pytest.mark.parametrize(
        "question, expected_topic",
        [
            ("how do for loops work in python", "For loop"),
            ("iterating over a list with a loop", "For loop"),
            ("what is variable scope in python", "Scope"),
            ("global and nonlocal statements", "Scope"),
            ("what is a decorator in python", "Decorator"),
            ("list comprehension syntax", "Comprehension"),
            ("string interpolation f-string", "String interpolation"),
            ("TypeError exception", "TypeError"),
            ("MRO", "MRO"),
            ("what is variable shadowing", "Variable shadowing"),
        ],
    )
    def test_phrasing_grounds_correctly(self, e2e_client, question, expected_topic):
        client, _ = e2e_client
        resp = _chat(client, question)
        assert resp.status_code == 200
        retrieval = resp.json()["usage"]["retrieval"]
        assert retrieval["topic"] == expected_topic, (
            f"Question {question!r}: expected {expected_topic!r}, "
            f"got {retrieval['topic']!r} (score={retrieval['score']:.3f})"
        )

    @pytest.mark.xfail(
        reason="Indirect phrasings that don't share vocabulary with the note "
        "body fail at TF-IDF retrieval. Known retrieval weakness.",
        strict=False,
    )
    @pytest.mark.parametrize(
        "question, expected_topic",
        [
            ("how does the @ symbol work on functions", "Decorator"),
            ("modifying a method with a wrapper", "Decorator"),
            ("what is a subclass superclass hierarchy", "Inheritance"),
            ("how to create a child class in python", "Inheritance"),
            ("is-a relationship between classes", "Inheritance"),
            ("shorthand for building a list from a loop", "Comprehension"),
            ("where can I use an identifier after initializing it", "Scope"),
        ],
    )
    def test_indirect_phrasing_grounds_correctly(self, e2e_client, question, expected_topic):
        client, _ = e2e_client
        resp = _chat(client, question)
        assert resp.status_code == 200
        retrieval = resp.json()["usage"]["retrieval"]
        assert retrieval["topic"] == expected_topic, (
            f"Question {question!r}: expected {expected_topic!r}, "
            f"got {retrieval['topic']!r} (score={retrieval['score']:.3f})"
        )


# ── Score confidence through the full stack ───────────────────────


MINIMUM_CONFIDENT_SCORE = 0.10


class TestE2EScoreConfidence:
    @pytest.mark.parametrize(
        "question",
        [
            "what is a for loop",
            "what is a decorator",
            "what is a dictionary",
            "what is variable scope",
            "what is encapsulation",
            "how does polymorphism work",
            "explain the self parameter",
            "what are boolean values",
        ],
    )
    def test_score_above_confidence_threshold(self, e2e_client, question):
        client, _ = e2e_client
        resp = _chat(client, question)
        assert resp.status_code == 200
        retrieval = resp.json()["usage"]["retrieval"]
        assert retrieval["score"] >= MINIMUM_CONFIDENT_SCORE, (
            f"Score {retrieval['score']:.4f} for {question!r} → "
            f"{retrieval['topic']!r} is below confidence threshold "
            f"{MINIMUM_CONFIDENT_SCORE} — grounding is fragile"
        )


# ── No-match handling ─────────────────────────────────────────────


class TestE2ENoMatch:
    def test_truly_empty_query_tokens_returns_no_topic(self, e2e_client):
        """A query where no token appears in the corpus vocabulary
        should produce topic=None."""
        client, _ = e2e_client
        # Use tokens that can't possibly appear in Python teaching notes
        resp = _chat(client, "zzzqqq xxxjjj")
        assert resp.status_code == 200
        retrieval = resp.json()["usage"]["retrieval"]
        assert retrieval["topic"] is None
        assert retrieval["score"] == 0.0

    def test_off_topic_still_returns_200(self, e2e_client):
        client, _ = e2e_client
        resp = _chat(client, "what is the meaning of life")
        assert resp.status_code == 200

    def test_no_match_system_prompt_still_has_tutor(self, e2e_client):
        """Even when retrieval fails, the tutor prompt should be present."""
        client, mock_claude = e2e_client
        mock_claude.reset_mock()
        _chat(client, "zzzqqq xxxjjj")
        system_prompt = mock_claude.messages.create.call_args.kwargs["system"]
        assert "Socratic" in system_prompt
